import os
from typing import Optional

import password_manager.application_context
from password_manager.encryption.key_derivator import KeyDerivator
from password_manager.file_helper import FileHelper
from password_manager.gui.create_database import CreateDatabaseDialog
from password_manager.gui.message_box import show_error
from password_manager.password_strength_validator import PasswordStrengthValidator


class CreateDatabaseController:
    def __init__(self, application_context: "password_manager.application_context.ApplicationContext") -> None:
        self.dialog = CreateDatabaseDialog()
        self.dialog.set_on_create(self._on_password_create_pressed)
        self.dialog.set_on_password_change(self._on_password_changed)
        self.dialog.set_on_open_existing_database(self._on_open_existing_pressed)
        self.application_context: password_manager.application_context.ApplicationContext = application_context

    def run_dialog(self) -> None:
        self.dialog.clear_fields()
        self.dialog.show()
        self.dialog.setFocus()
        self.dialog.browse_button.setFocus()

    def _on_password_create_pressed(self) -> None:
        if not self.dialog.are_passwords_matching():
            show_error("Passwords do not match")
            return
        password = self.dialog.get_password()
        if not password:
            show_error("Password cannot be empty")
            return
        path = self.dialog.get_database_path()
        if not path:
            show_error("Database location cannot be empty")
            return
        if not path.endswith('.pmdb'):
            path += ".pmdb"
        error = self._validate_path(path)
        if error:
            show_error(error)
            return

        self.application_context.initialize_database(path)
        if self.application_context.metadata_repository is None:
            raise ValueError("Metadata repository is not initialized")
        key = KeyDerivator(password, self.application_context.metadata_repository.get()).derive()
        self.application_context.initialize_data_access(key)
        self.dialog.hide()
        self.application_context.main_window_controller.run_window()

    @staticmethod
    def _validate_path(path: str) -> Optional[str]:
        dirname, basename = os.path.split(path)
        name = os.path.splitext(basename)
        if not name:
            return "Base name cannot be empty"
        if os.path.exists(path):
            return "File already exists"
        if not os.path.exists(dirname) or not os.path.isdir(dirname):
            return "Target directory does not exist"
        return None

    def _on_password_changed(self, password: str) -> None:
        self.dialog.set_strength_label(PasswordStrengthValidator().validate_password(password))

    def _on_open_existing_pressed(self) -> None:
        filename = FileHelper.open_db_file()
        if not filename:
            return
        self.application_context.initialize_database(filename)
        self.dialog.hide()
        self.application_context.login_controller.run_dialog()
