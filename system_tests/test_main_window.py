from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QLineEdit, QDialogButtonBox

from password_manager.controllers import main_window
from password_manager.utils.password_generator import GenerationOptions
from system_tests.fixture import SystemTestFixture


def test_main_window_add_record():
    with SystemTestFixture() as fixture:
        fixture.open_main_window_with_temp_db("res/empty.pmdb", "db.pmdb", "password")
        window = fixture.application_context.main_window_controller.window
        assert window.edit_save_button.text() == "Save"
        assert not window.edit_save_button.isEnabled()

        fixture.insert_text(window.title_input, "Title")
        fixture.insert_text(window.password_input, "Password")
        fixture.insert_text(window.login_input, "Login")
        fixture.insert_text(window.website_input, "Website")
        fixture.click_button(window.edit_save_button)
        assert window.record_list.count() == 1
        assert window.record_list.item(0).text() == "Title"


def test_main_window_controls_state():
    with SystemTestFixture() as fixture:
        fixture.open_main_window_with_temp_db("res/empty.pmdb", "db.pmdb", "password")
        window = fixture.application_context.main_window_controller.window

        inputs = [window.title_input, window.login_input, window.password_input, window.website_input,
                  window.login_url_input, window.description_input]
        assert window.edit_save_button.text() == "Save"
        assert not window.edit_save_button.isEnabled()
        assert all([not x.isReadOnly() for x in inputs])
        assert not window.add_new_button.isEnabled()
        assert not window.delete_button.isEnabled()

        fixture.insert_text(window.title_input, "Title")
        fixture.insert_text(window.password_input, "Password")
        assert window.edit_save_button.isEnabled()
        fixture.click_button(window.edit_save_button)
        assert all([x.isReadOnly() for x in inputs])
        assert window.add_new_button.isEnabled()
        assert window.delete_button.isEnabled()
        assert window.edit_save_button.text() == "Edit"


def test_main_window_search():
    with SystemTestFixture() as fixture:
        fixture.open_main_window_with_temp_db("res/empty.pmdb", "db.pmdb", "password")
        window = fixture.application_context.main_window_controller.window
        fixture.add_record("Title", "password")
        fixture.add_record("Other", "password")
        fixture.add_record("TitleOther", "password")
        assert window.record_list.count() == 3

        fixture.insert_text(window.search_input, "other")
        assert window.record_list.count() == 2
        assert window.record_list.item(0).text() == "Other"
        assert window.record_list.item(1).text() == "TitleOther"

        fixture.insert_text(window.search_input, "x")
        assert window.record_list.count() == 0


def test_main_window_delete():
    with SystemTestFixture() as fixture:
        fixture.open_main_window_with_temp_db("res/empty.pmdb", "db.pmdb", "password")
        window = fixture.application_context.main_window_controller.window
        fixture.add_record("Title", "password")
        fixture.add_record("Other", "password")
        assert window.record_list.count() == 2

        main_window.confirm = lambda _: True  # mock confirmation modal to return 'Yes'
        fixture.click_button(window.delete_button)
        assert window.record_list.count() == 1
        assert window.record_list.item(0).text() == 'Title'

        main_window.confirm = lambda _: False  # mock confirmation modal to return 'No'
        fixture.click_button(window.delete_button)
        assert window.record_list.count() == 1


def test_main_window_generate_password():
    with SystemTestFixture() as fixture:
        fixture.open_main_window_with_temp_db("res/empty.pmdb", "db.pmdb", "password")
        window = fixture.application_context.main_window_controller.window
        dialog = fixture.application_context.main_window_controller.password_dialog
        fixture.click_button(window.generate_button)
        assert dialog.isVisible()
        dialog.length_input.clear()
        fixture.insert_text(dialog.length_input, '22')
        fixture.click_button(dialog.buttons.button(QDialogButtonBox.StandardButton.Ok))
        assert not dialog.isVisible()
        assert len(window.password_input.text()) == 22


def test_main_window_copy_to_clipboard():
    with SystemTestFixture() as fixture:
        fixture.open_main_window_with_temp_db("res/empty.pmdb", "db.pmdb", "password")
        window = fixture.application_context.main_window_controller.window
        fixture.add_record("Title", "password")
        fixture.click_button(window.copy_button)
        assert QApplication.clipboard().text() == "password"


def test_main_window_show_password():
    with SystemTestFixture() as fixture:
        fixture.open_main_window_with_temp_db("res/empty.pmdb", "db.pmdb", "password")
        window = fixture.application_context.main_window_controller.window
        fixture.add_record("Title", "password")
        assert window.password_input.echoMode() == QLineEdit.EchoMode.Password
        fixture.click_button(window.show_button)
        assert window.password_input.echoMode() == QLineEdit.EchoMode.Normal


def test_main_window_preferences():
    with SystemTestFixture() as fixture:
        fixture.open_main_window_with_temp_db("res/empty.pmdb", "db.pmdb", "password")
        window = fixture.application_context.main_window_controller.window

        fixture.application_context.password_generation_options = GenerationOptions(True, True, True, True, "",
                                                                                    25)  # mock initial user preferences
        window.get_menubar().options_actions.trigger()
        dialog_preferences = fixture.application_context.main_window_controller.preferences_dialog
        assert dialog_preferences.isVisible()
        fixture.click_button(dialog_preferences.cancel_button)
        assert not dialog_preferences.isVisible()

        window.get_menubar().options_actions.trigger()
        QTest.qWaitForWindowExposed(dialog_preferences)
        dialog_preferences.lowercase_checkbox.setChecked(False)
        dialog_preferences.uppercase_checkbox.setChecked(False)
        fixture.click_button(dialog_preferences.save_button)
        assert not dialog_preferences.isVisible()

        dialog_generate = fixture.application_context.main_window_controller.password_dialog
        fixture.click_button(window.generate_button)
        assert dialog_generate.isVisible()
        assert not dialog_generate.uppercase_checkbox.isChecked()
        assert not dialog_generate.lowercase_checkbox.isChecked()
        assert dialog_generate.special_checkbox.isChecked()
        assert dialog_generate.numbers_checkbox.isChecked()
