from string import ascii_lowercase, ascii_uppercase, digits

from password_manager.utils.password_generator import PasswordGenerator, GenerationOptions

SpecialCharacters = '~!@#$%^&*()-=_+[{]}\\|;\':",.<>/?'


def test_alpha_password():
    password = PasswordGenerator.generate(GenerationOptions(False, False, False, True, "", 20))
    assert len(password) == 20
    assert all(char in ascii_lowercase for char in password)


def test_special_password():
    password = PasswordGenerator.generate(GenerationOptions(True, False, False, False, "", 15))
    assert len(password) == 15
    assert all(char in SpecialCharacters for char in password)


def test_custom_password():
    charset = '24680QAZPLM()!'
    password = PasswordGenerator.generate(GenerationOptions(False, False, False, False, charset, 22))
    assert len(password) == 22
    assert all(char in charset for char in password)


def test_multiple_options_password():
    password = PasswordGenerator.generate(GenerationOptions(True, True, True, True, "", 22))
    assert len(password) == 22
    assert any(char in ascii_lowercase for char in password)
    assert any(char in ascii_uppercase for char in password)
    assert any(char in SpecialCharacters for char in password)
    assert any(char in digits for char in password)
