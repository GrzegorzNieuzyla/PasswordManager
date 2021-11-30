import secrets
from dataclasses import dataclass
from string import digits, ascii_uppercase, ascii_lowercase
from typing import List, Set


@dataclass
class GenerationOptions:
    special: bool
    numbers: bool
    uppercase: bool
    lowercase: bool
    custom: str
    length: int


class PasswordGenerator:
    SpecialCharacters = '~!@#$%^&*()-=_+[{]}\\|;\':",.<>/?'

    @staticmethod
    def generate(options: GenerationOptions) -> str:
        """
        Generate password based on generation options
        """
        password: List[str] = []
        charset = PasswordGenerator._build_charset(options)
        while len(password) < options.length:
            password.append(secrets.choice(charset))

        used: Set[int] = set()
        if options.special:
            PasswordGenerator._patch(password, PasswordGenerator.SpecialCharacters, used, options.length)
        if options.numbers:
            PasswordGenerator._patch(password, digits, used, options.length)
        if options.uppercase:
            PasswordGenerator._patch(password, ascii_uppercase, used, options.length)
        if options.lowercase:
            PasswordGenerator._patch(password, ascii_lowercase, used, options.length)
        if options.custom:
            PasswordGenerator._patch(password, options.custom, used, options.length)

        return ''.join(password)

    @staticmethod
    def _build_charset(options: GenerationOptions) -> str:
        """
        Get all chars allowed for password creation
        """
        charset: Set[str] = set()
        if options.special:
            charset = charset.union(set(PasswordGenerator.SpecialCharacters))
        if options.numbers:
            charset = charset.union(set(digits))
        if options.uppercase:
            charset = charset.union(set(ascii_uppercase))
        if options.lowercase:
            charset = charset.union(set(ascii_lowercase))
        if options.custom:
            charset = charset.union(set(options.custom))

        return "".join(charset)

    @staticmethod
    def _patch(password: List[str], charset: str, used: Set[int], length: int) -> None:
        """
        Modify password that it contains at least one character from every option
        """
        ind = secrets.choice(range(length))
        while ind in used:
            ind = secrets.choice(range(length))
        used.add(ind)
        password[ind] = secrets.choice(charset)
