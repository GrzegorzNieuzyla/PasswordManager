from password_manager.utils.password_strength_validator import PasswordStrengthValidator, Strength


def test_validate_empty_password():
    assert PasswordStrengthValidator().validate_password("") == Strength.Empty


def test_validate_low_password():
    assert PasswordStrengthValidator().validate_password("password") == Strength.Low


def test_validate_medium_password():
    assert PasswordStrengthValidator().validate_password("!xzcA2F{%wA") == Strength.Medium


def test_validate_very_high_password():
    assert PasswordStrengthValidator().validate_password("J34$fsFs%[sasdc4562$#@[o}_c/>DAeds") == Strength.VeryHigh
