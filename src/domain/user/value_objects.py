import re
from dataclasses import dataclass

from domain.base.value_object import ValueObject
from domain.user.exceptions import (
    EmptyUsernameError,
    InvalidEmailFormatError,
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
