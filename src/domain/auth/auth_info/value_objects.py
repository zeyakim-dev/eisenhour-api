from dataclasses import dataclass, field
from enum import Enum

from domain.base.value_object import ValueObject


class AuthTypeEnum(Enum):
    """인증 방식의 종류를 나타내는 열거형.

    Values:
        LOCAL: 로컬 계정 기반 인증.
        GOOGLE: 구글 OAuth 기반 인증.
    """

    LOCAL = "LOCAL"
    GOOGLE = "GOOGLE"


@dataclass(frozen=True)
class AuthType(ValueObject[AuthTypeEnum]):
    """인증 방식 타입을 캡슐화하는 값 객체(Value Object).

    Attributes:
        value (AuthTypeEnum): 현재 인증 방식의 열거형 값.
    """

    value: AuthTypeEnum = field(default=AuthTypeEnum.LOCAL)

    def is_google(self) -> bool:
        """현재 인증 방식이 Google OAuth인지 확인한다.

        Returns:
            bool: Google OAuth이면 True, 아니면 False.
        """
        return self.value == AuthTypeEnum.GOOGLE

    def is_local(self) -> bool:
        """현재 인증 방식이 로컬 인증인지 확인한다.

        Returns:
            bool: 로컬 인증이면 True, 아니면 False.
        """
        return self.value == AuthTypeEnum.LOCAL


@dataclass(frozen=True)
class HashedPassword(ValueObject[str]):
    """해시 처리된 비밀번호를 표현하는 값 객체입니다.

    해싱된 문자열을 저장하며, 해시 비교 등의 용도로 사용됩니다.
    평문 비밀번호와는 다르며, 내부 값은 외부에서 직접 생성하거나 Hasher로 생성되어야 합니다.
    """

    pass
