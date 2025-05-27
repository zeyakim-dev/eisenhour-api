import pytest

from domain.auth.auth_info.local.value_objects import PlainPassword
from domain.user.exceptions import (
    PasswordMissingLowercaseError,
    PasswordMissingNumberError,
    PasswordMissingSpecialCharacterError,
    PasswordMissingUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
)


class TestPlainPasswordVO:
    def test_valid_password(self):
        assert PlainPassword("Abcd1234!").value == "Abcd1234!"

    def test_password_too_short(self):
        with pytest.raises(PasswordTooShortError):
            PlainPassword("A1a!")

    def test_password_too_long(self):
        with pytest.raises(PasswordTooLongError):
            PlainPassword("A" * 101 + "1a!")

    def test_missing_uppercase(self):
        with pytest.raises(PasswordMissingUppercaseError):
            PlainPassword("abcd1234!")

    def test_missing_lowercase(self):
        with pytest.raises(PasswordMissingLowercaseError):
            PlainPassword("ABCD1234!")

    def test_missing_number(self):
        with pytest.raises(PasswordMissingNumberError):
            PlainPassword("Abcdefgh!")

    def test_missing_special_character(self):
        with pytest.raises(PasswordMissingSpecialCharacterError):
            PlainPassword("Abcd1234")
