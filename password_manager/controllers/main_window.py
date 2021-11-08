from json import JSONDecodeError
from typing import Dict

from PyQt6.QtWidgets import QApplication

import password_manager.application_context
from password_manager.encryption.serializer import RecordSerializer
from password_manager.gui.main_window import MainWindow
from password_manager.logger import Logger
from password_manager.models.record_data import RecordData


class MainWindowController:
    def __init__(self, application_context: "password_manager.application_context.ApplicationContext"):
        self.window: MainWindow = MainWindow()
        self.application_context: "password_manager.application_context.ApplicationContext" = application_context
        self.records: Dict[int, RecordData] = {}
        self.current_record: int = -1
        self.window.set_on_copy(self._on_copy)
        self.window.set_on_add_new_record(self._on_add_new_record)
        self.window.set_on_delete(self._on_delete)
        self.window.set_on_update(self._on_update)
        self.window.set_on_generate(self._on_generate)

    def run_window(self):
        self.window.show()
        self.window.setFocus()

    def try_load_data(self) -> bool:
        if self.application_context.data_reader is None:
            raise ValueError("Data reader is not initialized")
        try:
            raw_records: Dict[int, bytes] = self.application_context.data_reader.get_all()
            self.records = RecordSerializer.deserialize_all(raw_records)
            Logger.info(f"Loaded records: {self.records}")
            return True
        except (JSONDecodeError, ValueError) as e:
            Logger.error(f"Main window controller: {e}")
            return False

    def _on_copy(self):
        if self.current_record > 0:
            QApplication.clipboard().setText(self.records[self.current_record].password)
            self.window.set_statusbar_text("Password copied to clipboard")
        else:
            self.window.set_statusbar_text("No active password to copy")

    def _on_add_new_record(self):
        pass

    def _on_delete(self):
        pass

    def _on_update(self):
        pass

    def _on_generate(self):
        pass
