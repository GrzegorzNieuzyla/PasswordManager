from typing import Callable

from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QSizePolicy, \
    QMainWindow, QPlainTextEdit, QListWidget, QGroupBox, QWidget, QStatusBar

from password_manager.gui.menubar import MenuBar
from password_manager.gui.password_strength_label import PasswordStrengthLabel
from password_manager.models.record_data import RecordData
from password_manager.password_strength_validator import Strength


class MainWindow(QMainWindow):
    def __init__(self):
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
        self.update_button: QPushButton = QPushButton("Update")
        self.generate_button: QPushButton = QPushButton("Generate")
        self.show_button: QPushButton = QPushButton("Show")
        self.copy_button: QPushButton = QPushButton("Copy")
        self.record_list: QListWidget = QListWidget()
        self.record_groupbox: QGroupBox = QGroupBox("Account data")
        self.menubar: MenuBar = MenuBar()
        self.setMenuBar(self.menubar)
        self.setStatusBar(QStatusBar())
        self._init_layout()
        self._init_properties()

    def _init_layout(self):
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
        bottom_box.addWidget(self.update_button)
        right_vbox.addLayout(bottom_box)

        self.record_groupbox.setLayout(right_vbox)
        main_layout.addWidget(self.record_groupbox)

    def _init_properties(self):
        self.resize(800, 700)
        self.setWindowTitle("Password manager")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.record_list.setFocus()
        self.set_strength_label(Strength.Low)

    def _on_show_clicked(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_button.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_button.setText("Show")

    def set_modification_time(self, days: int):
        if days > 1:
            self.modification_label.setText(f'Password set {days} ago')
        elif days == 1:
            self.modification_label.setText(f'Password set yesterday')
        else:
            self.modification_label.setText(f'Password set today')

    def set_on_add_new_record(self, callback: Callable[[], None]):
        self.add_new_button.clicked.connect(callback)  # type: ignore

    def set_on_delete(self, callback: Callable[[], None]):
        self.delete_button.clicked.connect(callback)  # type: ignore

    def set_on_update(self, callback: Callable[[], None]):
        self.update_button.clicked.connect(callback)  # type: ignore

    def set_on_copy(self, callback: Callable[[], None]):
        self.copy_button.clicked.connect(callback)  # type: ignore

    def set_on_generate(self, callback: Callable[[], None]):
        self.generate_button.clicked.connect(callback)  # type: ignore

    def set_strength_label(self, strength: Strength):
        self.strength_label.set_strength(strength)

    def set_on_search_changed(self, callback: Callable[[], str]):
        self.search_input.textEdited.connect(callback)  # type: ignore

    def get_data(self) -> RecordData:
        return RecordData(self.title_input.text(), self.website_input.text(), self.login_url_input.text(),
                          self.login_input.text(), self.password_input.text(), self.description_input.toPlainText(), 0)

    def clear_data(self):
        self.title_input.clear()
        self.website_input.clear()
        self.login_url_input.clear()
        self.login_input.clear()
        self.password_input.clear()
        self.description_input.clear()
        self.modification_label.clear()
        self.set_strength_label(Strength.Empty)

    def set_apply_button_text(self, text: str):
        self.update_button.setText(text)

    def get_menubar(self) -> MenuBar:
        return self.menubar
