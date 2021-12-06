from PyQt6.QtWidgets import QApplication
from pytest_mock import MockerFixture

from password_manager.application_context import ApplicationContext
from password_manager.controllers import create_database
from password_manager.controllers.create_database import CreateDatabaseController
from password_manager.utils.file_helper import FileHelper


def test_validation_passwords_not_matching(mocker: MockerFixture):
    _ = QApplication([])
    pass_matching = mocker.patch("password_manager.gui.create_database.CreateDatabaseDialog.are_passwords_matching")
    error = mocker.MagicMock('create_database.show_error')
    create_database.show_error = error
    pass_matching.return_value = False
    controller = CreateDatabaseController(ApplicationContext())
    controller._on_create_pressed()
    error.assert_called()


def test_validation_passwords_empty(mocker: MockerFixture):
    _ = QApplication([])
    pass_matching = mocker.patch("password_manager.gui.create_database.CreateDatabaseDialog.are_passwords_matching")
    get_password = mocker.patch("password_manager.gui.create_database.CreateDatabaseDialog.get_password")
    error = mocker.MagicMock('create_database.show_error')
    create_database.show_error = error
    pass_matching.return_value = True
    get_password.return_value = ''
    controller = CreateDatabaseController(ApplicationContext())
    controller._on_create_pressed()
    error.assert_called()


def test_validation_database_empty(mocker: MockerFixture):
    _ = QApplication([])
    pass_matching = mocker.patch("password_manager.gui.create_database.CreateDatabaseDialog.are_passwords_matching")
    get_password = mocker.patch("password_manager.gui.create_database.CreateDatabaseDialog.get_password")
    get_db = mocker.patch("password_manager.gui.create_database.CreateDatabaseDialog.get_database_path")
    error = mocker.MagicMock('create_database.show_error')
    create_database.show_error = error
    pass_matching.return_value = True
    get_db.return_value = ''
    get_password.return_value = 'password'
    controller = CreateDatabaseController(ApplicationContext())
    controller._on_create_pressed()
    error.assert_called()


def test_on_open_existing(mocker: MockerFixture):
    _ = QApplication([])
    context = ApplicationContext()
    context.login_controller.run_dialog = lambda: None
    init = mocker.patch("password_manager.application_context.ApplicationContext.initialize_database")
    FileHelper.open_db_file = lambda: "filename"
    controller = CreateDatabaseController(context)
    controller._on_open_existing_pressed()
    init.assert_called_with("filename")
