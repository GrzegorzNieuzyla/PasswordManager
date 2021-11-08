from json import JSONDecodeError
from typing import Dict, List

from PyQt6.QtWidgets import QApplication

import password_manager.application_context
from password_manager.gui.main_window import MainWindow
from password_manager.logger import Logger
from password_manager.models.record_data import RecordData


class MainWindowController:
    def __init__(self, application_context: "password_manager.application_context.ApplicationContext") -> None:
        self.window: MainWindow = MainWindow()
        self.application_context: "password_manager.application_context.ApplicationContext" = application_context
        self.records: List[RecordData] = []
        self.current_record: int = -1
        self.window.set_on_copy(self._on_copy)
        self.window.set_on_add_new_record(self._on_add_new_record)
        self.window.set_on_delete(self._on_delete)
        self.window.set_on_update(self._on_update)
        self.window.set_on_generate(self._on_generate)
        self.window.get_menubar().set_on_new_db(self._on_new_db)
        self.window.get_menubar().set_on_open_db(self._on_open_db)
        self.window.get_menubar().set_on_preferences(self._on_preferences)
        self.window.get_menubar().set_on_change_password(self._on_change_password)

    def run_window(self) -> None:
        self.window.show()
        self.window.setFocus()

    def try_load_data(self) -> bool:
        if self.application_context.data_reader is None:
            raise ValueError("Data reader is not initialized")
        try:
            raw_records: Dict[int, bytes] = self.application_context.data_reader.get_all()
            self.records = RecordData.deserialize_all(raw_records)
            Logger.info(f"Loaded records: {self.records}")
            return True
        except (JSONDecodeError, ValueError) as e:
            Logger.error(f"Main window controller: {e}")
            return False

    def _on_copy(self) -> None:
        if self.current_record > 0:
            QApplication.clipboard().setText(self.records[self.current_record].password)
            self.window.set_statusbar_text("Password copied to clipboard")
        else:
            self.window.set_statusbar_text("No active password to copy")

    def _on_add_new_record(self) -> None:
        pass

    def _on_delete(self) -> None:
        pass

    def _on_update(self) -> None:
        pass

    def _on_generate(self) -> None:
        pass

    def _on_new_db(self) -> None:
        pass

    def _on_open_db(self) -> None:
        pass

    def _on_preferences(self) -> None:
        pass

    def _on_change_password(self) -> None:
        pass
