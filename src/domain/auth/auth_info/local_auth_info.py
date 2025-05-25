from dataclasses import dataclass, field
from datetime import datetime, timedelta

from domain.auth.auth_info.auth_info import AuthInfo
from domain.auth.auth_info.exceptions import (
    PasswordChangeNotAllowedError,
    UserIdMismatchError,
)
from domain.auth.auth_info.value_objects import AuthType, AuthTypeEnum, HashedPassword
from domain.user.user import User
from shared_kernel.time.time_provider import TimeProvider


@dataclass(frozen=True, kw_only=True)
class LocalAuthInfo(AuthInfo):
    """로컬 인증 정보 객체.

    로컬 로그인 방식에서 비밀번호 검증, 변경, 만료 관리 책임을 갖는다.
    user_id를 기반으로 사용자와 연결되며, 불변성을 유지한다.
    """

    auth_type: AuthType = field(default_factory=lambda: AuthType(AuthTypeEnum.LOCAL))
    hashed_password: HashedPassword
    password_expired_at: datetime

    def validate_auth_type(self) -> bool:
        """인증 유형이 로컬인지 확인한다.

        Returns:
            bool: LOCAL 타입이면 True, 아니면 False.
        """
        return self.auth_type.is_local()

    def change_password(
        self, time_provider: TimeProvider, user: User, new_password: HashedPassword
    ) -> None:
        """비밀번호를 변경한다.

        사용자 ID와 인증 유형을 검증한 후, 새로운 비밀번호와 만료일자를 설정한다.

        Args:
            time_provider (TimeProvider): 현재 시간 제공자.
            user (User): 비밀번호 변경 요청 사용자.
            new_password (HashedPassword): 새롭게 설정할 해시된 비밀번호.

        Raises:
            UserIdMismatchError: user_id가 일치하지 않을 때.
            PasswordChangeNotAllowedError: 로컬이 아닌 인증에서 비밀번호 변경을 시도할 때.
        """
        if user.id != self.user_id:
            raise UserIdMismatchError(user.id, self.user_id)
        if user.auth_type != self.auth_type:  # type: ignore[attr-defined]
            raise PasswordChangeNotAllowedError(user.auth_type)  # type: ignore[attr-defined]

        expired_at = time_provider.now() + timedelta(days=90)
        self.update(
            time_provider, hashed_password=new_password, password_expired_at=expired_at
        )

    def is_password_expired(self, time_provider: TimeProvider) -> bool:
        """비밀번호가 만료되었는지 확인한다.

        Args:
            time_provider (TimeProvider): 현재 시간 제공자.

        Returns:
            bool: 만료일이 현재 시간보다 이전이면 True, 아니면 False.
        """
        return self.password_expired_at < time_provider.now()
