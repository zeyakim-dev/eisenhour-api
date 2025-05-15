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
from domain.user.value_objects import Email, Password, UserName


class TestUserNameVO:
    def test_valid_username(self):
        assert UserName("홍길동").value == "홍길동"

    def test_empty_username(self):
        with pytest.raises(EmptyUsernameError):
            UserName("")

    def test_whitespace_username(self):
        with pytest.raises(EmptyUsernameError):
            UserName("   ")

    def test_username_too_long(self):
        with pytest.raises(UsernameTooLongError):
            UserName("a" * 51)


class TestEmailVO:
    def test_valid_email(self):
        assert Email("user@example.com").value == "user@example.com"

    def test_invalid_email(self):
        with pytest.raises(InvalidEmailFormatError):
            Email("invalid-email")


class TestPasswordVO:
    def test_valid_password(self):
        assert Password("Abcd1234!").value == "Abcd1234!"

    def test_password_too_short(self):
        with pytest.raises(PasswordTooShortError):
            Password("A1a!")

    def test_password_too_long(self):
        with pytest.raises(PasswordTooLongError):
            Password("A" * 101 + "1a!")

    def test_missing_uppercase(self):
        with pytest.raises(PasswordMissingUppercaseError):
            Password("abcd1234!")

    def test_missing_lowercase(self):
        with pytest.raises(PasswordMissingLowercaseError):
            Password("ABCD1234!")

    def test_missing_number(self):
        with pytest.raises(PasswordMissingNumberError):
            Password("Abcdefgh!")

    def test_missing_special_character(self):
        with pytest.raises(PasswordMissingSpecialCharacterError):
            Password("Abcd1234")
