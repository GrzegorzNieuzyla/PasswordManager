from typing import Callable

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QSpacerItem

from password_manager.file_helper import FileHelper
from password_manager.gui.password_strength_label import PasswordStrengthLabel
from password_manager.password_strength_validator import Strength


class CreateDatabaseDialog(QDialog):
    def __init__(self):
        super(CreateDatabaseDialog, self).__init__()
        self.db_file_label: QLabel = QLabel("Database file location:")
        self.password_label: QLabel = QLabel("Master password: ")
        self.confirm_label: QLabel = QLabel("Confirm password:")
        self.strength_label: PasswordStrengthLabel = PasswordStrengthLabel()
        self.password_match_label: QLabel = QLabel()
        self.db_file_input: QLineEdit = QLineEdit()
        self.password_input: QLineEdit = QLineEdit()
        self.confirm_input: QLineEdit = QLineEdit()
        self.open_existing_button: QPushButton = QPushButton("Open existing database")
        self.browse_button: QPushButton = QPushButton("Browse")
        self.show_button: QPushButton = QPushButton("Show")
        self.create_button: QPushButton = QPushButton("Create")
        self._init_layout()
        self._init_properties()

    def _init_layout(self):
        main_layout = QVBoxLayout(self)

        file_box = QHBoxLayout()
        file_box.addWidget(self.db_file_label)
        file_box.addWidget(self.db_file_input)
        file_box.addWidget(self.browse_button)
        main_layout.addLayout(file_box)
        main_layout.addItem(QSpacerItem(40, 20))

        password_box = QHBoxLayout()
        password_box.addWidget(self.password_label)
        password_box.addWidget(self.password_input)
        password_box.addWidget(self.show_button)
        main_layout.addLayout(password_box)
        main_layout.addItem(QSpacerItem(40, 10))

        confirm_box = QHBoxLayout()
        confirm_box.addWidget(self.confirm_label)
        confirm_box.addWidget(self.confirm_input)
        main_layout.addLayout(confirm_box)
        main_layout.addItem(QSpacerItem(40, 20))
        main_layout.addWidget(self.password_match_label)
        label_box = QHBoxLayout()
        label_box.addWidget(self.strength_label)
        main_layout.addLayout(label_box)
        main_layout.addItem(QSpacerItem(40, 20))

        button_box = QHBoxLayout()
        button_box.addWidget(self.open_existing_button)
        button_box.addItem(QSpacerItem(80, 20))
        button_box.addWidget(self.create_button)
        main_layout.addLayout(button_box)

    def _init_properties(self):
        self.resize(600, 280)
        self.setWindowTitle("Create password database")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.show_button.clicked.connect(self._on_show_clicked)
        self.browse_button.clicked.connect(self._on_browse_clicked)
        self.password_input.textEdited.connect(self._on_password_changed)
        self.confirm_input.textEdited.connect(self._on_password_changed)
        self.create_button.setEnabled(False)

    def _on_browse_clicked(self):
        filename: str = FileHelper.open_db_file_for_writing()
        if filename:
            self.db_file_input.setText(filename)

    def _on_show_clicked(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_button.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_button.setText("Show")

    def _on_password_changed(self):
        password: str = self.password_input.text()
        confirm: str = self.confirm_input.text()
        if (password or confirm) and password != confirm:
            self.password_match_label.setText('<span style="color:red;">Passwords do not match!</span>')
        else:
            self.password_match_label.clear()
        self.create_button.setEnabled(self.are_passwords_matching() and len(self.password_input.text()) > 0)

    def get_password(self) -> str:
        return self.password_input.text()

    def set_strength_label(self, strength: Strength):
        self.strength_label.set_strength(strength)

    def get_database_path(self) -> str:
        return self.db_file_input.text()

    def set_on_create(self, callback: Callable[[], None]):
        self.create_button.clicked.connect(callback)  # type: ignore

    def set_on_open_existing_database(self, callback: Callable[[], None]):
        self.open_existing_button.clicked.connect(callback)  # type: ignore

    def set_on_password_change(self, callback: Callable[[str], None]):
        self.password_input.textEdited.connect(callback)  # type: ignore

    def are_passwords_matching(self) -> bool:
        return self.password_input.text() == self.confirm_input.text()

    def clear_fields(self):
        self.password_input.clear()
        self.confirm_input.clear()
        self.set_strength_label(Strength.Empty)
        self.create_button.setEnabled(False)
