import os.path

from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QLineEdit

from password_manager.utils.file_helper import FileHelper
from system_tests.fixture import SystemTestFixture


def test_create_database_dialog_controls_state():
    with SystemTestFixture() as fixture:
        dialog = fixture.application_context.create_database_controller.dialog
        assert not dialog.create_button.isEnabled()

        db_file = fixture.get_db_file("db.pmdb")
        fixture.insert_text(dialog.db_file_input, db_file)
        assert not dialog.create_button.isEnabled()

        assert not dialog.create_button.isEnabled()

        fixture.insert_text(dialog.password_input, "password")
        fixture.insert_text(dialog.confirm_input, "password2")
        assert not dialog.create_button.isEnabled()

        QTest.keyClick(dialog.confirm_input, Qt.Key.Key_Backspace, delay=fixture.delay)
        assert dialog.create_button.isEnabled()

        fixture.click_button(dialog.show_button)
        assert dialog.password_input.echoMode() == QLineEdit.EchoMode.Normal and dialog.confirm_input.echoMode() == QLineEdit.EchoMode.Normal


def test_create_database_dialog_database_creation():
    with SystemTestFixture() as fixture:
        dialog = fixture.application_context.create_database_controller.dialog
        db_file = fixture.get_db_file("db.pmdb")
        fixture.insert_text(dialog.db_file_input, db_file)
        fixture.insert_text(dialog.password_input, "password")
        fixture.insert_text(dialog.confirm_input, "password")
        fixture.click_button(dialog.create_button)
        assert os.path.exists(db_file)

        QTest.qWaitForWindowExposed(
            fixture.application_context.main_window_controller.window)  # wait for key derivation
        assert fixture.application_context.main_window_controller.window.isVisible()


def test_create_database_dialog_existing_database():
    with SystemTestFixture() as fixture:
        dialog = fixture.application_context.create_database_controller.dialog
        db_file = fixture.get_filepath("res/empty.pmdb")
        FileHelper.open_db_file = lambda: db_file
        fixture.click_button(dialog.open_existing_button)
        QTest.qWaitForWindowExposed(fixture.application_context.login_controller.dialog)

        assert fixture.application_context.login_controller.dialog.isVisible()
        assert fixture.application_context.login_controller.dialog.current_db_label.text().endswith(db_file)
