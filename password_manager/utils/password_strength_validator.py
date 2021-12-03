import math
from enum import Enum
from string import ascii_lowercase, ascii_uppercase, digits


class Strength(Enum):
    Empty = 0,
    VeryLow = 1,
    Low = 2,
    Medium = 3
    High = 4
    VeryHigh = 5


class PasswordStrengthValidator:
    SpecialCharacters = '~!@#$%^&*()-=_+[{]}\\|;\':",.<>/?'

    def validate_password(self, password: str) -> Strength:
        """
        Check password and return the strength description
        """
        special: bool = len(set(self.SpecialCharacters).union(set(password))) > 0
        numbers: bool = len(set(digits).union(set(password))) > 0
        uppercase: bool = len(set(ascii_uppercase).union(set(password))) > 0
        lowercase: bool = len(set(ascii_lowercase).union(set(password))) > 0
        return self.validate(special, numbers, uppercase, lowercase, len(password))

    def validate(self, special: bool, numbers: bool, uppercase: bool, lowercase: bool, length: int,
                 custom: str = "") -> Strength:
        """
        Check generation options and return the strength description
        """
        characters = set()
        if special:
            for char in self.SpecialCharacters:
                characters.add(char)
        if numbers:
            for char in digits:
                characters.add(char)
        if uppercase:
            for char in ascii_uppercase:
                characters.add(char)
        if lowercase:
            for char in ascii_lowercase:
                characters.add(char)
        if custom:
            for char in custom:
                characters.add(char)

        entropy = self._calculate_entropy(len(characters), length)

        if entropy == 0:
            return Strength.Empty
        elif entropy < 20:
            return Strength.VeryLow
        elif entropy < 70:
            return Strength.Low
        elif entropy < 120:
            return Strength.Medium
        elif entropy < 200:
            return Strength.High
        else:
            return Strength.VeryHigh

    @staticmethod
    def _calculate_entropy(pool_size: int, length: int) -> float:
        if pool_size == 0:
            return 0.0
        return length * math.log2(pool_size)
