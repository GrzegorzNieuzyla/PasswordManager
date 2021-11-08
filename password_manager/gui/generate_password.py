from dataclasses import dataclass
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QDialogButtonBox, QCheckBox, QSlider, \
    QSpinBox

from password_manager.gui.password_strength_label import PasswordStrengthLabel
from password_manager.password_strength_validator import Strength


@dataclass
class GenerationOptions:
    special: bool
    numbers: bool
    uppercase: bool
    lowercase: bool
    custom: str
    length: int


class GeneratePasswordDialog(QDialog):
    def __init__(self) -> None:
        super(GeneratePasswordDialog, self).__init__()
        self.strength_label: PasswordStrengthLabel = PasswordStrengthLabel()
        self.length_label: QLabel = QLabel("Password length:")
        self.special_checkbox: QCheckBox = QCheckBox("Special characters")
        self.numbers_checkbox: QCheckBox = QCheckBox("Numbers")
        self.uppercase_checkbox: QCheckBox = QCheckBox("Uppercase letters")
        self.lowercase_checkbox: QCheckBox = QCheckBox("Lowercase letters")
        self.custom_checkbox: QCheckBox = QCheckBox("Custom")
        self.custom_input: QLineEdit = QLineEdit()
        self.buttons: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.length_slider: QSlider = QSlider(Qt.Orientation.Horizontal)
        self.length_input: QSpinBox = QSpinBox()
        self._init_layout()
        self._init_properties()

    def _init_layout(self) -> None:
        main_layout = QVBoxLayout(self)

        main_layout.addWidget(self.special_checkbox)
        main_layout.addWidget(self.numbers_checkbox)
        main_layout.addWidget(self.uppercase_checkbox)
        main_layout.addWidget(self.lowercase_checkbox)

        custom_box = QHBoxLayout()
        custom_box.addWidget(self.custom_checkbox)
        custom_box.addWidget(self.custom_input)
        main_layout.addLayout(custom_box)

        length_box = QHBoxLayout()
        length_box.addWidget(self.length_label)
        length_box.addWidget(self.length_slider)
        length_box.addWidget(self.length_input)
        main_layout.addLayout(length_box)

        main_layout.addWidget(self.strength_label)
        main_layout.addWidget(self.buttons)

    def _init_properties(self) -> None:
        self.resize(360, 300)
        self.setWindowTitle("Generate password")
        self.buttons.rejected.connect(self.close)  # type: ignore
        self.length_input.valueChanged.connect(self._on_spinbox_value_change)  # type: ignore
        self.length_slider.valueChanged.connect(self._on_slider_value_change)  # type: ignore
        self.custom_checkbox.stateChanged.connect(self._on_custom_checkbox_changed)  # type: ignore
        self.length_slider.setMinimum(5)
        self.length_slider.setMaximum(100)
        self.length_input.setMinimum(5)
        self.length_input.setMaximum(100)
        self.special_checkbox.setChecked(True)
        self.numbers_checkbox.setChecked(True)
        self.uppercase_checkbox.setChecked(True)
        self.lowercase_checkbox.setChecked(True)
        self.custom_checkbox.setChecked(False)
        self.custom_input.setEnabled(False)

    def _on_custom_checkbox_changed(self) -> None:
        self.custom_input.setEnabled(self.custom_checkbox.isChecked())

    def _on_slider_value_change(self, value: int) -> None:
        self.length_input.setValue(value)

    def _on_spinbox_value_change(self, value: int) -> None:
        self.length_slider.setValue(value)

    def get_options(self) -> GenerationOptions:
        return GenerationOptions(self.special_checkbox.isChecked(), self.numbers_checkbox.isChecked(),
                                 self.uppercase_checkbox.isChecked(), self.lowercase_checkbox.isChecked(),
                                 self.custom_input.text() if self.custom_checkbox.isChecked() else "",
                                 int(self.length_input.value()))

    def set_on_ok(self, callback: Callable[[], None]) -> None:
        self.buttons.accepted.connect(callback)  # type: ignore

    def set_strength_label(self, strength: Strength) -> None:
        self.strength_label.set_strength(strength)
