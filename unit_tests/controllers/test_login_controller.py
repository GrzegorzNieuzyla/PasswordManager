from PyQt6.QtWidgets import QApplication
from pytest_mock import MockerFixture

import password_manager.controllers.login
from password_manager.utils.file_helper import FileHelper


def test_on_change_db(mocker: MockerFixture):
    _ = QApplication([])
    dialog_mock = mocker.MagicMock()
    mocker.patch('password_manager.controllers.login.LoginDialog', return_value=dialog_mock)
    context = mocker.MagicMock()
    controller = password_manager.controllers.login.LoginController(context)
    filename = 'filename.pmdb'
    FileHelper.open_db_file = lambda: filename
    controller._on_change_db_pressed()
    dialog_mock.set_database_label.assert_called_with(filename)
    context.initialize_database.assert_called_with(filename)
