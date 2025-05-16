import pytest

from domain.user.exceptions import (
    EmptyUsernameError,
    InvalidEmailFormatError,
    PasswordMissingLowercaseError,
    PasswordMissingNumberError,
    PasswordMissingSpecialCharacterError,
    PasswordMissingUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
    UsernameTooLongError,
)
from domain.user.value_objects import Email, PlainPassword, Username


class TestUsernameVO:
    def test_valid_username(self):
        assert Username("홍길동").value == "홍길동"

    def test_empty_username(self):
        with pytest.raises(EmptyUsernameError):
            Username("")

    def test_whitespace_username(self):
        with pytest.raises(EmptyUsernameError):
            Username("   ")

    def test_username_too_long(self):
        with pytest.raises(UsernameTooLongError):
            Username("a" * 51)


class TestEmailVO:
    def test_valid_email(self):
        assert Email("user@example.com").value == "user@example.com"

    def test_invalid_email(self):
        with pytest.raises(InvalidEmailFormatError):
            Email("invalid-email")


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
