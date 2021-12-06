from PyQt6.QtTest import QTest

from system_tests.fixture import SystemTestFixture


def test_login_dialog_controls_state():
    with SystemTestFixture() as fixture:
        db = fixture.get_filepath("res/empty.pmdb")
        fixture.open_existing_database(db)
        dialog = fixture.application_context.login_controller.dialog
        assert dialog.new_db_button.isEnabled()
        assert not dialog.open_button.isEnabled()
        fixture.insert_text(dialog.password_input, "password")
        assert dialog.open_button.isEnabled()


def test_login_create_new():
    with SystemTestFixture() as fixture:
        db = fixture.get_filepath("res/empty.pmdb")
        fixture.open_existing_database(db)
        dialog = fixture.application_context.login_controller.dialog
        fixture.click_button(dialog.new_db_button)
        assert fixture.application_context.create_database_controller.dialog.isVisible()
        assert not dialog.isVisible()


def test_login_open_db():
    with SystemTestFixture() as fixture:
        dialog = fixture.application_context.login_controller.dialog
        db = fixture.get_filepath("res/database.pmdb")
        fixture.open_existing_database(db)
        fixture.insert_text(dialog.password_input, "password")
        fixture.click_button(dialog.open_button)
        QTest.qWaitForWindowExposed(
            fixture.application_context.main_window_controller.window)  # wait for key derivation
        window = fixture.application_context.main_window_controller.window
        assert window.isVisible()
        assert window.record_list.count() == 1


def test_login_open_db_incorrect_password():
    with SystemTestFixture() as fixture:
        dialog = fixture.application_context.login_controller.dialog
        db = fixture.get_filepath("res/database.pmdb")
        fixture.open_existing_database(db)
        fixture.insert_text(dialog.password_input, "password2")
        fixture.click_button(dialog.open_button)
        QTest.qWaitForWindowExposed(
            fixture.application_context.main_window_controller.window)  # wait for key derivation
        window = fixture.application_context.main_window_controller.window
        assert not window.isVisible()
        assert dialog.wrong_password_label.text()
