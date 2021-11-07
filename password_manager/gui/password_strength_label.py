from enum import Enum

from PyQt6.QtWidgets import QLabel


class PasswordStrengthLabel(QLabel):
    class Strength(Enum):
        Empty = 0,
        VeryLow = 1,
        Low = 2,
        Medium = 3
        High = 4
        VeryHigh = 5

    def __init__(self):
        super(PasswordStrengthLabel, self).__init__()

    def set_strength(self, strength: Strength):
        if strength == self.Strength.VeryLow:
            self._set_strength("Very low ", "DarkRed")
        elif strength == self.Strength.Low:
            self._set_strength("Low      ", "Crimson")
        elif strength == self.Strength.Medium:
            self._set_strength("Medium   ", "Orange")
        elif strength == self.Strength.High:
            self._set_strength("High     ", "GreenYellow")
        elif strength == self.Strength.VeryHigh:
            self._set_strength("Very high", "Green")
        else:
            self._set_strength("         ", "Green")

    def _set_strength(self, text: str, color: str):
        self.setText(f'Password strength: <span style="color: {color};">{text}</span>')
