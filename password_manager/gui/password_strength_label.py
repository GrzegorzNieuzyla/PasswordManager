from PyQt6.QtWidgets import QLabel

from password_manager.utils.password_strength_validator import Strength


class PasswordStrengthLabel(QLabel):
    """
    A GUI element showing the strength of a password
    """

    def __init__(self) -> None:
        super(PasswordStrengthLabel, self).__init__()

    def set_strength(self, strength: Strength) -> None:
        if strength == Strength.VeryLow:
            self._set_strength("Very low ", "DarkRed")
        elif strength == Strength.Low:
            self._set_strength("Low      ", "Crimson")
        elif strength == Strength.Medium:
            self._set_strength("Medium   ", "Orange")
        elif strength == Strength.High:
            self._set_strength("High     ", "GreenYellow")
        elif strength == Strength.VeryHigh:
            self._set_strength("Very high", "Green")
        else:
            self._set_strength("         ", "Green")

    def _set_strength(self, text: str, color: str) -> None:
        self.setText(f'Password strength: <span style="color: {color};">{text}</span>')
