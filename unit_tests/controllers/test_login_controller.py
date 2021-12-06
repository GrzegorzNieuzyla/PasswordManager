import pytest
from PyQt6.QtWidgets import QApplication
from pytest_mock import MockerFixture

from password_manager.application_context import ApplicationContext
from password_manager.controllers.login import LoginController
from password_manager.utils.file_helper import FileHelper


def test_on_change_db(mocker: MockerFixture):
    _ = QApplication([])
    dialog_mock = mocker.MagicMock()
    mocker.patch('password_manager.controllers.login.LoginDialog', return_value=dialog_mock)
    context = mocker.MagicMock()
    controller = LoginController(context)
    filename = 'filename.pmdb'
    FileHelper.open_db_file = lambda: filename
    controller._on_change_db_pressed()
    dialog_mock.set_database_label.assert_called_with(filename)
    context.initialize_database.assert_called_with(filename)


def test_exception_without_database():
    _ = QApplication([])
    context = ApplicationContext()
    controller = LoginController(context)
    with pytest.raises(ValueError):
        controller.run_dialog()


def test_on_new_db(mocker: MockerFixture):
    _ = QApplication([])
    mock = mocker.patch('password_manager.controllers.create_database.CreateDatabaseController.run_dialog')
    context = ApplicationContext()
    controller = LoginController(context)
    controller.dialog.new_db_button.click()
    mock.assert_called()
