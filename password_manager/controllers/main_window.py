import time
from enum import Enum
from json import JSONDecodeError
from typing import Dict, Optional

from PyQt6.QtWidgets import QApplication

import password_manager.application_context
from password_manager.gui.generate_password import GeneratePasswordDialog
from password_manager.gui.main_window import MainWindow
from password_manager.gui.message_box import confirm
from password_manager.models.record_data import RecordData
from password_manager.utils.logger import Logger
from password_manager.utils.password_generator import PasswordGenerator
from password_manager.utils.password_strength_validator import PasswordStrengthValidator


class MainWindowController:
    class State(Enum):
        View = 0
        Update = 1
        New = 2

    def __init__(self, application_context: "password_manager.application_context.ApplicationContext") -> None:
        self.window: MainWindow = MainWindow()
        self.password_dialog: GeneratePasswordDialog = GeneratePasswordDialog()
        self.application_context: "password_manager.application_context.ApplicationContext" = application_context
        self.records: Dict[int, RecordData] = {}
        self.current_record: Optional[RecordData] = None
        self.state: MainWindowController.State = self.State.New

        self.window.set_on_copy(self._on_copy)
        self.window.set_on_add_new_record(self._on_add_new_record)
        self.window.set_on_delete(self._on_delete)
        self.window.set_on_save_edit(self._on_save_edit)
        self.window.set_on_generate(self._on_generate)
        self.window.get_menubar().set_on_new_db(self._on_new_db)
        self.window.get_menubar().set_on_open_db(self._on_open_db)
        self.window.get_menubar().set_on_preferences(self._on_preferences)
        self.window.record_list.set_on_clicked(self._on_item_clicked)
        self.window.record_list.set_on_double_clicked(self._on_item_double_clicked)
        self.window.set_on_search_changed(self._on_search_changed)
        self.window.set_on_password_change(self._on_password_changed)
        self.password_dialog.set_on_ok(self._on_password_generation)
        self.window.set_update_state(True)

    def run_window(self) -> None:
        self.window.show()
        self.window.setFocus()

    def try_load_data(self) -> bool:
        try:
            self.window.clear_data()
            raw_records: Dict[int, bytes] = self.application_context.get_data_reader().get_all()
            self.records = RecordData.deserialize_all(raw_records)
            for record in self.records.values():
                self.window.record_list.add_record(record)
            self.window.record_list.clearSelection()
            Logger.info(f"Loaded records: {self.records}")
            return True
        except (JSONDecodeError, ValueError) as e:
            Logger.error(f"Main window controller: {e}")
            return False

    def load_new_db(self) -> None:
        self.window.clear_data()

    def _on_copy(self) -> None:
        if self.current_record is not None:
            QApplication.clipboard().setText(self.current_record.password)
            self.window.set_statusbar_text(f"Password for {self.current_record.title} copied to clipboard")
        else:
            self.window.set_statusbar_text("No active password to copy")

    def _on_add_new_record(self) -> None:
        if self.state == self.State.New:
            return
        self.current_record = None
        self.window.record_list.clearSelection()
        self.state = self.State.New
        self.window.clear_data(clear_records=False)
        self.window.set_update_state(True)

    def _on_delete(self) -> None:
        if self.state in (self.State.View, self.State.Update) and self.current_record is not None:
            if not confirm(f"Remove record {self.current_record.title}?"):
                return
            self.application_context.get_data_writer().delete(self.current_record.id_)
            self.window.record_list.remove_record(self.current_record)
            del self.records[self.current_record.id_]

    def _on_save_edit(self) -> None:
        if self.state == self.State.View:
            self.window.set_update_state(False)
            self.state = self.State.Update
        elif self.state == self.State.New:
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
        self.password_dialog.clear()
        self.password_dialog.show()

    def _on_new_db(self) -> None:
        self.application_context.create_database_controller.run_dialog()

    def _on_open_db(self) -> None:
        self.application_context.login_controller.run_dialog()

    def _on_preferences(self) -> None:
        pass

    def _on_password_changed(self, password: str) -> None:
        self.window.set_strength_label(PasswordStrengthValidator().validate_password(password))

    def _on_search_changed(self, query: str) -> None:
        self.window.record_list.filter(query)

    def _on_item_clicked(self, record: RecordData) -> None:
        self.current_record = record
        self.window.set_data(record)
        self.state = self.State.View
        self.window.set_view_state()

    def _on_item_double_clicked(self, record: RecordData) -> None:
        QApplication.clipboard().setText(record.password)
        self.window.set_statusbar_text(f"Password for {record.title} copied to clipboard")

    def _on_password_generation(self) -> None:
        options = self.password_dialog.get_options()
        password = PasswordGenerator.generate(options)
        self.window.password_input.setText(password)
        self._on_password_changed(password)
        self.password_dialog.clear()
        self.password_dialog.hide()
