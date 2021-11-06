from typing import Callable

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt


class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()
        self.current_db_label: QLabel = QLabel()
        self.password_label: QLabel = QLabel("Master password:")
        self.wrong_password_label: QLabel = QLabel()
        self.password_input: QLineEdit = QLineEdit()
        self.open_button: QPushButton = QPushButton("Open")
        self.change_db_button: QPushButton = QPushButton("Change database")
        self.new_db_button: QPushButton = QPushButton("Create new database")
        self._init_layout()
        self._init_properties()

    def _init_layout(self):
        main_layout = QVBoxLayout(self)

        top_label_box = QHBoxLayout()
        top_label_box.addItem(QSpacerItem(40, 20))
        top_label_box.addWidget(self.current_db_label)
        self.current_db_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_label_box.addItem(QSpacerItem(40, 20))
        main_layout.addLayout(top_label_box)

        password_box = QHBoxLayout()
        password_box.addWidget(self.password_label)
        password_box.addWidget(self.password_input)
        main_layout.addLayout(password_box)
        main_layout.addItem(QSpacerItem(40, 50))

        main_layout.addWidget(self.wrong_password_label)
        self.wrong_password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons_box = QHBoxLayout()
        buttons_box.addWidget(self.change_db_button)
        buttons_box.addWidget(self.new_db_button)
        buttons_box.addWidget(self.open_button)

        self.change_db_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.new_db_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.open_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        main_layout.addLayout(buttons_box)

    def _init_properties(self):
        self.resize(500, 200)
        self.setWindowTitle("Open database")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFocus()

    def get_password(self) -> str:
        return self.password_input.text()

    def set_database_label(self, label: str):
        self.current_db_label.setText(f"Current database file: {label}")

    def set_on_change_db(self, callback: Callable[[], None]):
        self.change_db_button.clicked.connect(callback)  # type: ignore

    def set_on_open(self, callback: Callable[[], None]):
        self.open_button.clicked.connect(callback)  # type: ignore
        self.password_input.returnPressed.connect(callback)  # type: ignore

    def set_on_new_db(self, callback: Callable[[], None]):
        self.new_db_button.textEdited.connect(callback)  # type: ignore

    def set_incorrect_password(self, incorrect: bool):
        self.wrong_password_label.setText(
            '<span style="color:red;">Password incorrect or corrupted database</span>' if incorrect else "")
