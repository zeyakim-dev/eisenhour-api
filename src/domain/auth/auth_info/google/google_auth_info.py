from dataclasses import dataclass, field

from domain.auth.auth_info.base.auth_info import AuthInfo
from domain.auth.auth_info.base.value_objects import AuthType, AuthTypeEnum
from domain.auth.auth_info.google.value_objects import GoogleSub


@dataclass(frozen=True, kw_only=True)
class GoogleAuthInfo(AuthInfo):
    """
    Google OAuth 기반 인증 정보 객체.

    - Google OAuth의 sub(고유 식별자), email, 프로필 이미지 등 보유
    - user_id를 기반으로 사용자와 연결됨
    - 불변성을 유지하며, 인증 타입은 항상 GOOGLE
    """

    auth_type: AuthType = field(default_factory=lambda: AuthType(AuthTypeEnum.GOOGLE))
    sub: GoogleSub
    avatar_url: str | None

    def validate_auth_type(self) -> bool:
        """
        인증 유형이 GOOGLE인지 확인합니다.

        Returns:
            bool: GOOGLE 타입이면 True, 아니면 False
        """
        return self.auth_type.is_google()
