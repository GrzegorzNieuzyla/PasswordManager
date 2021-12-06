from PyQt6.QtWidgets import QApplication
from pytest_mock import MockerFixture

from password_manager.application_context import ApplicationContext
from password_manager.controllers.main_window import MainWindowController
from password_manager.models.record_data import RecordData


def get_context() -> ApplicationContext:
    context = ApplicationContext()
    context.run_server = False
    context.save_preferences = False
    return context


def get_records():
    return {
        2: RecordData(0, "Title1", "https://website1.com", "loginurl1.com", "Login1", "Password1", "Description1",
                      2).serialize(),
        3: RecordData(0, "Title2", "https://website2.com", "loginurl2.com", "Login2", "Password2", "Description2",
                      3).serialize()
    }


def test_load_data_success(mocker: MockerFixture):
    _ = QApplication([])
    context = get_context()
    controller = MainWindowController(context)
    records = get_records()
    context.data_reader = mocker.MagicMock()
    context.data_reader.get_all = lambda: records
    assert controller.try_load_data()


def test_load_data_failure(mocker: MockerFixture):
    _ = QApplication([])
    context = get_context()
    controller = MainWindowController(context)
    records = {2: b'not a json'}
    context.data_reader = mocker.MagicMock()
    context.data_reader.get_all = lambda: records
    assert not controller.try_load_data()


def test_integration_get_sites():
    _ = QApplication([])
    context = get_context()
    controller = MainWindowController(context)
    records = get_records()
    controller.records = {2: RecordData.deserialize(records[2], 2)}
    assert controller._on_integration_get_sites() == ['loginurl1.com']


def test_integration_get_password():
    _ = QApplication([])
    context = get_context()
    controller = MainWindowController(context)
    records = get_records()
    controller.records = {2: RecordData.deserialize(records[2], 2)}
    assert controller._on_integration_get_password("loginurl1.com") == [('Login1', 'Password1')]


def test_save_on_view_state():
    _ = QApplication([])
    context = get_context()
    controller = MainWindowController(context)
    controller.state = MainWindowController.State.View
    controller._on_save_edit()
    assert controller.state == MainWindowController.State.Update


def test_save_on_new_state(mocker: MockerFixture):
    _ = QApplication([])
    context = get_context()
    controller = MainWindowController(context)
    controller.state = MainWindowController.State.New
    context.data_writer = mocker.MagicMock()
    context.data_writer.add = lambda _: 2
    controller._on_save_edit()
    assert controller.state == MainWindowController.State.View


def test_save_on_update_state(mocker: MockerFixture):
    _ = QApplication([])
    context = get_context()
    controller = MainWindowController(context)
    controller.state = MainWindowController.State.New
    controller.records = {2: RecordData.deserialize(get_records()[2], 2)}
    context.data_writer = mocker.MagicMock()
    context.data_writer.update = lambda _: None
    controller.current_record = controller.records[2]

    controller._on_save_edit()
    assert controller.state == MainWindowController.State.View


def test_clear_url():
    assert MainWindowController.clear_url("https://example.com/resources?a=b") == "example.com"
    assert MainWindowController.clear_url("example.com/resources?a=b") == "example.com"
    assert MainWindowController.clear_url("https://example.com") == "example.com"
