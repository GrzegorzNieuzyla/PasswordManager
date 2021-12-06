from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QCheckBox, QLineEdit, QSlider, QSpinBox, QVBoxLayout, QHBoxLayout, \
    QPushButton

from password_manager.utils.password_generator import GenerationOptions


class PreferencesDialog(QDialog):
    def __init__(self) -> None:
        super(PreferencesDialog, self).__init__()
        self.passwords_title_label: QLabel = QLabel("Password generation default options")
        self.length_label: QLabel = QLabel("Password length:")
        self.special_checkbox: QCheckBox = QCheckBox("Special characters")
        self.numbers_checkbox: QCheckBox = QCheckBox("Numbers")
        self.uppercase_checkbox: QCheckBox = QCheckBox("Uppercase letters")
        self.lowercase_checkbox: QCheckBox = QCheckBox("Lowercase letters")
        self.custom_checkbox: QCheckBox = QCheckBox("Custom")
        self.save_button: QPushButton = QPushButton("Save")
        self.cancel_button: QPushButton = QPushButton("Cancel")
        self.custom_input: QLineEdit = QLineEdit()
        self.length_slider: QSlider = QSlider(Qt.Orientation.Horizontal)
        self.length_input: QSpinBox = QSpinBox()
        self._init_layout()
        self._init_properties()

    def _init_layout(self) -> None:
        """
        Create controls and place them in layout on window
        """
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.passwords_title_label)

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

        button_box = QHBoxLayout()
        button_box.addWidget(self.cancel_button)
        button_box.addWidget(self.save_button)
        main_layout.addLayout(button_box)

    def _init_properties(self) -> None:
        """
        Set options and setup callbacks
        """
        self.resize(360, 300)
        self.setWindowTitle("User preferences")
        self.length_slider.setMinimum(5)
        self.length_slider.setMaximum(100)
        self.length_input.setMinimum(5)
        self.length_input.setMaximum(100)

        self.length_input.valueChanged.connect(self._on_spinbox_value_change)  # type: ignore
        self.length_slider.valueChanged.connect(self._on_slider_value_change)  # type: ignore
        self.custom_checkbox.stateChanged.connect(self._on_custom_checkbox_changed)  # type: ignore
        self.cancel_button.clicked.connect(self.close)  # type: ignore
        self.uppercase_checkbox.stateChanged.connect(self._on_input_changes)  # type: ignore
        self.lowercase_checkbox.stateChanged.connect(self._on_input_changes)  # type: ignore
        self.special_checkbox.stateChanged.connect(self._on_input_changes)  # type: ignore
        self.numbers_checkbox.stateChanged.connect(self._on_input_changes)  # type: ignore
        self.custom_input.textEdited.connect(self._on_input_changes)  # type: ignore

    def _on_custom_checkbox_changed(self) -> None:
        self.custom_input.setEnabled(self.custom_checkbox.isChecked())
        self._on_input_changes()

    def _on_slider_value_change(self, value: int) -> None:
        self.length_input.setValue(value)
        self._on_input_changes()

    def _on_spinbox_value_change(self, value: int) -> None:
        self.length_slider.setValue(value)
        self._on_input_changes()

    def run_dialog(self, options: GenerationOptions) -> None:
        self.set_options(options)
        self.show()

    def set_on_save(self, callback: Callable[[], None]) -> None:
        self.save_button.clicked.connect(callback)  # type: ignore

    def get_options(self) -> GenerationOptions:
        return GenerationOptions(self.special_checkbox.isChecked(), self.numbers_checkbox.isChecked(),
                                 self.uppercase_checkbox.isChecked(), self.lowercase_checkbox.isChecked(),
                                 self.custom_input.text() if self.custom_checkbox.isChecked() else "",
                                 int(self.length_input.value()))

    def set_options(self, options: GenerationOptions) -> None:
        self.special_checkbox.setChecked(options.special)
        self.numbers_checkbox.setChecked(options.numbers)
        self.uppercase_checkbox.setChecked(options.uppercase)
        self.lowercase_checkbox.setChecked(options.lowercase)
        self.custom_checkbox.setChecked(len(options.custom) > 0)
        self.custom_input.setEnabled(len(options.custom) > 0)
        self.custom_input.setText(options.custom)
        self.length_input.setValue(options.length)
        self.length_slider.setValue(options.length)

    def _on_input_changes(self):
        options = self.get_options()
        self.save_button.setEnabled(
            len(options.custom) or options.special or options.numbers or options.lowercase or options.uppercase)
