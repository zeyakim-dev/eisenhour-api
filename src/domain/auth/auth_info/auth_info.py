from abc import abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.auth.auth_info.exceptions import InvalidAuthTypeError
from domain.auth.auth_info.value_objects import AuthType
from domain.base.aggregate import Aggregate


@dataclass(frozen=True, kw_only=True)
class AuthInfo(Aggregate):
    """
    인증 정보의 공통 애그리거트 루트.

    사용자 ID와 인증 방식을 캡슐화하며,
    하위 클래스에서 구체 인증 방식별 유효성을 보장한다.
    """

    user_id: UUID
    auth_type: AuthType

    def __post_init__(self) -> None:
        """
        인스턴스 생성 시 인증 타입의 유효성을 검증한다.

        Raises:
            InvalidAuthTypeError: auth_type이 하위 클래스에서 요구하는 값과 일치하지 않을 때 발생.
        """
        if not self.validate_auth_type():
            raise InvalidAuthTypeError(self.auth_type)

    @abstractmethod
    def validate_auth_type(self) -> bool:
        """
        하위 클래스에서 인증 타입의 유효성을 검증하도록 강제한다.

        Returns:
            bool: 유효하면 True, 아니면 False.
        """
        raise NotImplementedError

    def is_google_auth(self) -> bool:
        """
        현재 인증 타입이 Google OAuth인지 확인한다.

        Returns:
            bool: Google OAuth이면 True.
        """
        return self.auth_type.is_google()

    def is_local_auth(self) -> bool:
        """
        현재 인증 타입이 Local 인증인지 확인한다.

        Returns:
            bool: Local 인증이면 True.
        """
        return self.auth_type.is_local()
