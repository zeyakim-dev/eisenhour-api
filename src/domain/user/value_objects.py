import re
from dataclasses import dataclass

from domain.base.value_object import ValueObject
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


@dataclass(frozen=True)
class UserName(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not self.value or len(self.value.strip()) == 0:
            raise EmptyUsernameError()
        if len(self.value) > 50:
            raise UsernameTooLongError()


@dataclass(frozen=True)
class Email(ValueObject):
    value: str

    def __post_init__(self) -> None:
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, self.value):
            raise InvalidEmailFormatError()


@dataclass(frozen=True)
class PlainPassword(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < 8:
            raise PasswordTooShortError()
        if len(self.value) > 100:
            raise PasswordTooLongError()
        if not re.search(r"[A-Z]", self.value):
            raise PasswordMissingUppercaseError()
        if not re.search(r"[a-z]", self.value):
            raise PasswordMissingLowercaseError()
        if not re.search(r"[0-9]", self.value):
            raise PasswordMissingNumberError()
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.value):
            raise PasswordMissingSpecialCharacterError()


@dataclass(frozen=True)
class HashedPassword(ValueObject):
    value: str
