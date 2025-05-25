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
class Username(ValueObject[str]):
    """사용자의 고유 이름을 표현하는 값 객체입니다.

    공백이거나 비어있을 수 없으며, 최대 50자까지 허용됩니다.
    불변성을 가지며 문자열 기반으로 동등성과 해시가 정의됩니다.

    Raises:
        EmptyUsernameError: 값이 비어있거나 공백만 포함된 경우.
        UsernameTooLongError: 50자를 초과한 경우.
    """

    def __post_init__(self) -> None:
        if not self.value or len(self.value.strip()) == 0:
            raise EmptyUsernameError()
        if len(self.value) > 50:
            raise UsernameTooLongError()


@dataclass(frozen=True)
class Email(ValueObject[str]):
    """사용자의 이메일 주소를 표현하는 값 객체입니다.

    '@' 기호와 도메인 구문이 포함된 유효한 이메일 형식이어야 합니다.
    문자열 기반의 값 비교 및 해시가 가능하며, 불변성을 유지합니다.

    Raises:
        InvalidEmailFormatError: 이메일 형식이 잘못된 경우.
    """

    def __post_init__(self) -> None:
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, self.value):
            raise InvalidEmailFormatError()


@dataclass(frozen=True)
class PlainPassword(ValueObject[str]):
    """사용자가 입력한 평문 비밀번호를 표현하는 값 객체입니다.

    비밀번호는 다음 보안 조건을 모두 충족해야 합니다:
    - 8자 이상 100자 이하
    - 대문자, 소문자, 숫자, 특수문자 포함

    유효하지 않은 경우 각 조건에 따라 예외를 발생시키며, 해시 전 검증에 사용됩니다.

    Raises:
        PasswordTooShortError: 8자 미만인 경우.
        PasswordTooLongError: 100자 초과인 경우.
        PasswordMissingUppercaseError: 대문자가 없는 경우.
        PasswordMissingLowercaseError: 소문자가 없는 경우.
        PasswordMissingNumberError: 숫자가 없는 경우.
        PasswordMissingSpecialCharacterError: 특수문자가 없는 경우.
    """

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
