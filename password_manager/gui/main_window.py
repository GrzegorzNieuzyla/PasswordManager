from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QSizePolicy, \
    QMainWindow, QPlainTextEdit, QGroupBox, QWidget, QStatusBar

from password_manager.gui.menubar import MenuBar
from password_manager.gui.password_strength_label import PasswordStrengthLabel
from password_manager.gui.record_list import RecordList
from password_manager.models.record_data import RecordData
from password_manager.utils.password_strength_validator import Strength


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.title_label: QLabel = QLabel("Title:")
        self.login_label: QLabel = QLabel("Login:")
        self.password_label: QLabel = QLabel("Password:")
        self.website_label: QLabel = QLabel("Website:")
        self.login_url_label: QLabel = QLabel("Login URL:")
        self.description_label: QLabel = QLabel("Description:")
        self.search_label: QLabel = QLabel("Search:")
        self.modification_label: QLabel = QLabel()
        self.strength_label: PasswordStrengthLabel = PasswordStrengthLabel()

        self.search_input: QLineEdit = QLineEdit()
        self.title_input: QLineEdit = QLineEdit()
        self.login_input: QLineEdit = QLineEdit()
        self.password_input: QLineEdit = QLineEdit()
        self.website_input: QLineEdit = QLineEdit()
        self.login_url_input: QLineEdit = QLineEdit()
        self.description_input: QPlainTextEdit = QPlainTextEdit()

        self.add_new_button: QPushButton = QPushButton("Add new record")
        self.delete_button: QPushButton = QPushButton("Delete")
        self.edit_save_button: QPushButton = QPushButton("Update")
        self.generate_button: QPushButton = QPushButton("Generate")
        self.show_button: QPushButton = QPushButton("Show")
        self.copy_button: QPushButton = QPushButton("Copy")
        self.record_list: RecordList = RecordList()
        self.record_groupbox: QGroupBox = QGroupBox("Account data")
        self.menubar: MenuBar = MenuBar()
        self.setMenuBar(self.menubar)
        self.setStatusBar(QStatusBar())
        self._init_layout()
        self._init_properties()

    def _init_layout(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_vbox = QVBoxLayout()
        search_box = QHBoxLayout()
        search_box.addWidget(self.search_label)
        search_box.addWidget(self.search_input)
        left_vbox.addLayout(search_box)
        left_vbox.addWidget(self.record_list)
        left_vbox.addWidget(self.add_new_button)
        main_layout.addLayout(left_vbox)

        right_vbox = QVBoxLayout()
        title_box = QHBoxLayout()
        title_box.addWidget(self.title_label)
        title_box.addWidget(self.title_input)
        right_vbox.addLayout(title_box)

        login_box = QHBoxLayout()
        login_box.addWidget(self.login_label)
        login_box.addWidget(self.login_input)
        right_vbox.addLayout(login_box)
        self.record_list.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        self.search_input.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self.search_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        password_box = QHBoxLayout()
        password_box.addWidget(self.password_label)
        password_box.addWidget(self.password_input)
        right_vbox.addLayout(password_box)
        self.add_new_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        buttons_box = QHBoxLayout()
        buttons_box.addWidget(self.strength_label)
        buttons_box.addWidget(self.generate_button)
        buttons_box.addWidget(self.show_button)
        buttons_box.addWidget(self.copy_button)
        right_vbox.addLayout(buttons_box)

        website_box = QHBoxLayout()
        website_box.addWidget(self.website_label)
        website_box.addWidget(self.website_input)
        right_vbox.addLayout(website_box)

        url_box = QHBoxLayout()
        url_box.addWidget(self.login_url_label)
        url_box.addWidget(self.login_url_input)
        right_vbox.addLayout(url_box)

        right_vbox.addWidget(self.description_label)
        right_vbox.addWidget(self.description_input)

        bottom_box = QHBoxLayout()
        bottom_box.addWidget(self.modification_label)
        bottom_box.addWidget(self.delete_button)
        bottom_box.addWidget(self.edit_save_button)
        right_vbox.addLayout(bottom_box)

        self.record_groupbox.setLayout(right_vbox)
        main_layout.addWidget(self.record_groupbox)

    def _init_properties(self) -> None:
        self.resize(800, 700)
        self.setWindowTitle("Password manager")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.record_list.setFocus()
        self.set_strength_label(Strength.Low)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.show_button.clicked.connect(self._on_show_clicked)  # type: ignore

    def _on_show_clicked(self) -> None:
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_button.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_button.setText("Show")

    def set_modification_time(self, days: int) -> None:
        if days > 1:
            self.modification_label.setText(f'Password set {days} ago')
        elif days == 1:
            self.modification_label.setText(f'Password set yesterday')
        else:
            self.modification_label.setText(f'Password set today')

    def set_on_add_new_record(self, callback: Callable[[], None]) -> None:
        self.add_new_button.clicked.connect(callback)  # type: ignore

    def set_on_delete(self, callback: Callable[[], None]) -> None:
        self.delete_button.clicked.connect(callback)  # type: ignore

    def set_on_save_edit(self, callback: Callable[[], None]) -> None:
        self.edit_save_button.clicked.connect(callback)  # type: ignore

    def set_on_copy(self, callback: Callable[[], None]) -> None:
        self.copy_button.clicked.connect(callback)  # type: ignore

    def set_on_generate(self, callback: Callable[[], None]) -> None:
        self.generate_button.clicked.connect(callback)  # type: ignore

    def set_strength_label(self, strength: Strength) -> None:
        self.strength_label.set_strength(strength)

    def set_on_search_changed(self, callback: Callable[[str], None]) -> None:
        self.search_input.textEdited.connect(callback)  # type: ignore

    def set_on_password_change(self, callback: Callable[[str], None]) -> None:
        self.password_input.textEdited.connect(callback)  # type: ignore

    def get_data(self) -> RecordData:
        return RecordData(-1, self.title_input.text(), self.website_input.text(), self.login_url_input.text(),
                          self.login_input.text(), self.password_input.text(), self.description_input.toPlainText(), 0)

    def set_data(self, record: RecordData) -> None:
        self.title_input.setText(record.title)
        self.website_input.setText(record.website)
        self.login_url_input.setText(record.loginUrl)
        self.login_input.setText(record.login)
        self.password_input.setText(record.password)
        self.description_input.setPlainText(record.description)
        self.set_modification_time(record.get_days_from_modification())

    def clear_data(self, clear_records: bool = True) -> None:
        self.title_input.clear()
        self.website_input.clear()
        self.login_url_input.clear()
        self.login_input.clear()
        self.password_input.clear()
        self.description_input.clear()
        self.modification_label.clear()
        self.set_strength_label(Strength.Empty)
        if clear_records:
            self.record_list.clear_data()

    def set_apply_button_text(self, text: str) -> None:
        self.edit_save_button.setText(text)

    def get_menubar(self) -> MenuBar:
        return self.menubar

    def set_statusbar_text(self, text: str, seconds: int = 10) -> None:
        self.statusBar().showMessage(text, seconds * 1000)

    def _enable_inputs(self, enabled: bool) -> None:
        self.search_input.setReadOnly(not enabled)
        self.title_input.setReadOnly(not enabled)
        self.login_input.setReadOnly(not enabled)
        self.password_input.setReadOnly(not enabled)
        self.website_input.setReadOnly(not enabled)
        self.login_url_input.setReadOnly(not enabled)
        self.description_input.setReadOnly(not enabled)

    def set_update_state(self, new_record: bool) -> None:
        self.add_new_button.setEnabled(False)
        self.delete_button.setEnabled(not new_record)
        self.edit_save_button.setEnabled(True)
        self.edit_save_button.setText("Save")
        self._enable_inputs(True)

    def set_view_state(self) -> None:
        self.add_new_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.edit_save_button.setEnabled(True)
        self.edit_save_button.setText("Edit")
        self._enable_inputs(False)
