import re
from dataclasses import dataclass

from domain.auth.auth_info.local.exceptions import (
    PasswordMissingLowercaseError,
    PasswordMissingNumberError,
    PasswordMissingSpecialCharacterError,
    PasswordMissingUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
)
from domain.base.value_object import ValueObject


@dataclass(frozen=True)
class HashedPassword(ValueObject[str]):
    """해시 처리된 비밀번호를 표현하는 값 객체입니다.

    해싱된 문자열을 저장하며, 해시 비교 등의 용도로 사용됩니다.
    평문 비밀번호와는 다르며, 내부 값은 외부에서 직접 생성하거나 Hasher로 생성되어야 합니다.
    """

    pass


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
