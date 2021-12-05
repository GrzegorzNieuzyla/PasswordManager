import os

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from password_manager.application_context import ApplicationContext
from password_manager.utils.file_helper import FileHelper


class SystemTestFixture:
    def __init__(self, delay: int = 0):
        self.delay = delay
        self.app = QApplication([])
        self.application_context = ApplicationContext()
        self.application_context.run_server = False
        self.application_context.initialize_integration_server(self.get_filepath('test_key.pem'),
                                                               self.get_filepath('test_cert.pem'), 20000)
        self.application_context.create_database_controller.run_dialog()
        self.db_file = None
        QTest.qWait(500)

    @staticmethod
    def get_filepath(name: str) -> str:
        return f'{os.path.dirname(os.path.realpath(__file__))}/{name}'

    def get_db_file(self, name: str) -> str:
        self.db_file = self.get_filepath(name)
        return self.db_file

    def click_button(self, button):
        QTest.mouseClick(button, Qt.MouseButton.LeftButton, delay=self.delay * 5)

    def insert_text(self, widget, text):
        QTest.keyClicks(widget, text, delay=self.delay)

    def __enter__(self):
        return self

    def __exit__(self, _, __, ___):
        if self.db_file and os.path.exists(self.db_file):
            os.remove(self.db_file)

    def open_existing_database(self, filepath):
        FileHelper.open_db_file = lambda: filepath
        self.click_button(self.application_context.create_database_controller.dialog.open_existing_button)
