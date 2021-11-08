import password_manager.application_context
from password_manager.encryption.key_derivator import KeyDerivator
from password_manager.file_helper import FileHelper
from password_manager.gui.login_dialog import LoginDialog


class LoginController:
    def __init__(self, application_context: "password_manager.application_context.ApplicationContext"):
        self.dialog: LoginDialog = LoginDialog()
        self.application_context: "password_manager.application_context.ApplicationContext" = application_context
        self.dialog.set_on_open(self._on_open_pressed)
        self.dialog.set_on_new_db(self._on_new_db_pressed)
        self.dialog.set_on_change_db(self._on_change_db_pressed)

    def run_dialog(self):
        self.dialog.clear_fields()
        self.dialog.show()
        self.dialog.set_database_label(self.application_context.database_manager.path)
        self.dialog.setFocus()
        self.dialog.password_input.setFocus()

    def _on_open_pressed(self):
        password = self.dialog.get_password()
        if not password:
            return
        key = KeyDerivator(password, self.application_context.metadata_repository.get()).derive()
        self.application_context.initialize_data_access(key)
        if not self.application_context.main_window_controller.try_load_data():
            self.dialog.set_incorrect_password(True)
            return
        self.dialog.hide()
        self.application_context.main_window_controller.run_window()

    def _on_new_db_pressed(self):
        self.dialog.hide()
        self.application_context.create_database_controller.run_dialog()

    def _on_change_db_pressed(self):
        filename = FileHelper.open_db_file()
        if not filename:
            return
        self.dialog.set_database_label(filename)
        self.application_context.initialize_database(filename)
        self.dialog.clear_fields()
