"""
Google 인증 관련 값 객체 정의.

GoogleSub: Google OAuth의 sub(고유 식별자) 값 객체.
"""

from dataclasses import dataclass

from domain.auth.auth_info.google.exceptions import (
    GoogleSubEmptyError,
    GoogleSubTooLongError,
)


@dataclass(frozen=True)
class GoogleSub:
    """
    Google OAuth의 sub(고유 식별자) 값 객체.

    - 비어 있거나 공백일 수 없음
    - 최대 128자 제한
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise GoogleSubEmptyError(self.value)
        if len(self.value) > 128:
            raise GoogleSubTooLongError(self.value, 128)
