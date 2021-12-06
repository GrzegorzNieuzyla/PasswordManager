import os
from shutil import copyfile

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

from password_manager.application_context import ApplicationContext
from password_manager.utils.file_helper import FileHelper


class SystemTestFixture:
    def __init__(self, delay: int = 10):
        self.delay = delay
        self.app = QApplication([])
        self.application_context = ApplicationContext()
        self.application_context.run_server = False
        self.application_context.save_preferences = False
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

    def open_main_window_with_temp_db(self, db_file: str, new_db: str, password: str):
        file = self.get_db_file(new_db)
        copyfile(self.get_filepath(db_file), file)
        self.open_existing_database(file)
        self.insert_text(self.application_context.login_controller.dialog.password_input, password)
        self.click_button(self.application_context.login_controller.dialog.open_button)
        QTest.qWait(2000)

    def open_existing_database(self, filepath: str):
        FileHelper.open_db_file = lambda: filepath
        self.click_button(self.application_context.create_database_controller.dialog.open_existing_button)

    def add_record(self, title: str, password: str):
        self.click_button(self.application_context.main_window_controller.window.add_new_button)
        self.insert_text(self.application_context.main_window_controller.window.title_input, title)
        self.insert_text(self.application_context.main_window_controller.window.password_input, password)
        self.click_button(self.application_context.main_window_controller.window.edit_save_button)
