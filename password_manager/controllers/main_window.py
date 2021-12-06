import time
from enum import Enum
from json import JSONDecodeError
from os import _exit
from typing import Dict, Optional, List, Tuple
from urllib.parse import urlparse

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication

import password_manager.application_context
from password_manager.gui.generate_password import GeneratePasswordDialog
from password_manager.gui.main_window import MainWindow
from password_manager.gui.message_box import confirm
from password_manager.gui.preferences_dialog import PreferencesDialog
from password_manager.integration.controller import IntegrationController
from password_manager.models.record_data import RecordData
from password_manager.utils.logger import Logger
from password_manager.utils.options import set_generation_options
from password_manager.utils.password_generator import PasswordGenerator
from password_manager.utils.password_strength_validator import PasswordStrengthValidator


class MainWindowController:
    class State(Enum):
        """
        Enum indicating the inner state of main window
        """
        View = 0
        Update = 1
        New = 2

    def __init__(self, application_context: "password_manager.application_context.ApplicationContext") -> None:
        self.window: MainWindow = MainWindow()
        self.password_dialog: GeneratePasswordDialog = GeneratePasswordDialog()
        self.preferences_dialog: PreferencesDialog = PreferencesDialog()
        self.application_context: "password_manager.application_context.ApplicationContext" = application_context
        self.records: Dict[int, RecordData] = {}
        self.current_record: Optional[RecordData] = None
        self.state: MainWindowController.State = self.State.New
        self.integration_controller: Optional[IntegrationController] = None
        self._add_record_signal = pyqtSignal(RecordData)
        self._server_running = False

        self.window.set_on_copy(self._on_copy)
        self.window.set_on_add_new_record(self._on_add_new_record)
        self.window.set_on_delete(self._on_delete)
        self.window.set_on_save_edit(self._on_save_edit)
        self.window.set_on_generate(self._on_generate)
        self.window.get_menubar().set_on_new_db(self._on_new_db)
        self.window.get_menubar().set_on_open_db(self._on_open_db)
        self.window.get_menubar().set_on_options(self._on_preferences)
        self.preferences_dialog.set_on_save(self._on_preferences_save)
        self.window.record_list.set_on_clicked(self._on_item_clicked)
        self.window.record_list.set_on_double_clicked(self._on_item_double_clicked)
        self.window.set_on_search_changed(self._on_search_changed)
        self.window.set_on_password_change(self._on_password_changed)
        self.password_dialog.set_on_ok(self._on_password_generation)
        self.window.set_update_state(True)
        self.window.set_on_close(self.on_close)

    def run_window(self) -> None:
        self.window.show()
        self.window.setFocus()

    def try_load_data(self) -> bool:
        """
        Try to decrypt records based on previously obtained key
        """
        try:
            self.window.clear_data()
            raw_records: Dict[int, bytes] = self.application_context.get_data_reader().get_all()
            self.records = RecordData.deserialize_all(raw_records)
            for record in self.records.values():
                self.window.record_list.add_record(record)
            self.window.record_list.clearSelection()
            Logger.info(f"Loaded records: {self.records}")
            self.run_integration_server()
            return True
        except (JSONDecodeError, ValueError) as e:
            Logger.error(f"Main window controller: {e}")
            return False

    def load_new_db(self) -> None:
        self.window.clear_data()

    def _setup_integration(self) -> None:
        if self.integration_controller:
            self.integration_controller.set_get_sites_handler(self._on_integration_get_sites)
            self.integration_controller.set_get_password_handler(self._on_integration_get_password)
            self.integration_controller.set_create_password_handler(self._on_integration_create_password)
            self.integration_controller.start_server()

    def _on_integration_get_sites(self) -> List[str]:
        sites = map(lambda x: x.loginUrl if self.clear_url(x.loginUrl) else x.website, self.records.values())
        return list(filter(None, sites))

    def _on_integration_get_password(self, url: str) -> List[Tuple[str, str]]:
        result = []
        url = self.clear_url(url)
        for record in self.records.values():
            if record.loginUrl:
                if self.clear_url(record.loginUrl) == url:
                    result.append((record.login, record.password))
            elif record.website:
                if self.clear_url(record.website) == url:
                    result.append((record.login, record.password))
        return result

    def _on_integration_create_password(self, url: str, login: str) -> str:
        password = PasswordGenerator().generate(self.application_context.password_generation_options)
        clear_url = self.clear_url(url)

        record = RecordData(-1, f'{clear_url} - {login}', clear_url, url, login, password, f'Password for {clear_url}',
                            int(time.time()))
        record.id_ = self.application_context.get_data_writer().add(record.serialize())
        self.records[record.id_] = record
        self.window.record_list.add_record_signal.emit(record)
        return password

    @staticmethod
    def clear_url(url: str) -> str:
        if not url.startswith('http'):
            url = f'https://{url}'
        return urlparse(url).netloc

    def _on_copy(self) -> None:
        """
        Copy password to clipboard
        """
        if self.current_record is not None:
            QApplication.clipboard().setText(self.current_record.password)
            self.window.set_statusbar_text(f"Password for {self.current_record.title} copied to clipboard")
        else:
            self.window.set_statusbar_text("No active password to copy")

    def _on_add_new_record(self) -> None:
        """
        Disable readonly on input controls and go into add state
        """
        if self.state == self.State.New:
            return
        self.current_record = None
        self.window.record_list.clearSelection()
        self.state = self.State.New
        self.window.clear_data(clear_records=False)
        self.window.set_update_state(True)

    def _on_delete(self) -> None:
        """
        Ask for confirmation and delete record
        """
        if self.state in (self.State.View, self.State.Update) and self.current_record is not None:
            if not confirm(f"Remove record {self.current_record.title}?"):
                return
            self.application_context.get_data_writer().delete(self.current_record.id_)
            self.window.record_list.remove_record(self.current_record)
            del self.records[self.current_record.id_]
            self.window.clear_data(False)
            self.window.set_update_state(True)
            self.window.record_list.setFocus()

    def _on_save_edit(self) -> None:
        if self.state == self.State.View:
            # Go into update mode for current record
            self.window.set_update_state(False)
            self.state = self.State.Update
        elif self.state == self.State.New:
            # Save current input data to a new record
            new_record: RecordData = self.window.get_data()
            new_record.modificationDate = int(time.time())
            new_record.id_ = self.application_context.get_data_writer().add(new_record.serialize())
            self.window.record_list.add_record(new_record)
            self.records[new_record.id_] = new_record
            self.current_record = new_record
            self.state = self.State.View
            self.window.set_view_state()
            self.window.clear_filters()
        elif self.state == self.State.Update and self.current_record is not None:
            # Update current record with given data
            current_id = self.current_record.id_
            updated_record: RecordData = self.window.get_data()
            updated_record.modificationDate = int(time.time())
            self.application_context.get_data_writer().update(self.current_record.id_, updated_record.serialize())

            self.window.record_list.remove_record(self.current_record)
            updated_record.id_ = current_id
            self.records[current_id] = updated_record
            self.current_record = updated_record
            self.window.record_list.add_record(updated_record)

            self.state = self.State.View
            self.window.set_view_state()

    def _on_generate(self) -> None:
        """
        Show password generation dialog
        """
        self.password_dialog.run_dialog(self.application_context.password_generation_options)

    def _on_preferences(self) -> None:
        self.preferences_dialog.run_dialog(self.application_context.password_generation_options)

    def _on_preferences_save(self) -> None:
        self.application_context.password_generation_options = self.preferences_dialog.get_options()
        set_generation_options(self.application_context.password_generation_options)
        self.preferences_dialog.close()

    def _on_new_db(self) -> None:
        self.application_context.create_database_controller.run_dialog()

    def _on_open_db(self) -> None:
        self.application_context.login_controller.run_dialog()

    def _on_password_changed(self, password: str) -> None:
        self.window.set_strength_label(PasswordStrengthValidator().validate_password(password))

    def _on_search_changed(self, query: str) -> None:
        self.window.record_list.filter(query)

    def _on_item_clicked(self, record: RecordData) -> None:
        self.current_record = record
        self.window.set_data(record)
        self.state = self.State.View
        self.window.set_view_state()
        self._on_password_changed(self.window.password_input.text())

    def _on_item_double_clicked(self, record: RecordData) -> None:
        """
        Copy to clipboard
        """
        QApplication.clipboard().setText(record.password)
        self.window.set_statusbar_text(f"Password for {record.title} copied to clipboard")

    def _on_password_generation(self) -> None:
        """
        Generate password based on options from password generation dialog
        """
        options = self.password_dialog.get_options()
        password = PasswordGenerator.generate(options)
        self.window.password_input.setText(password)
        self._on_password_changed(password)
        self.password_dialog.clear()
        self.password_dialog.hide()
        self.window.on_input_changed()

    def run_integration_server(self) -> None:
        if self._server_running or not self.application_context.run_server:
            return
        self.integration_controller = self.application_context.get_integration_controller()
        self._setup_integration()
        self._server_running = True

    @staticmethod
    def on_close() -> None:
        _exit(0)
