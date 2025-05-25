from uuid import UUID

from domain.auth.auth_info.value_objects import AuthType


class InvalidAuthTypeError(Exception):
    """잘못된 인증 타입이 사용되었을 때 발생하는 예외.

    Attributes:
        auth_type (AuthType): 잘못 주입된 인증 타입 값.
    """

    def __init__(self, auth_type: AuthType) -> None:
        """InvalidAuthTypeError를 생성한다.

        Args:
            auth_type (AuthType): 잘못 주입된 인증 타입 값.
        """
        super().__init__(f"Invalid auth type: {auth_type.value.value}")


class UserIdMismatchError(Exception):
    """사용자 ID가 일치하지 않을 때 발생하는 예외.

    Attributes:
        user_id (UUID): 사용자 ID.
    """

    def __init__(self, user_id: UUID, auth_info_user_id: UUID) -> None:
        super().__init__(f"User ID mismatch: {user_id} != {auth_info_user_id}")


class PasswordChangeNotAllowedError(Exception):
    """비밀번호 변경이 허용되지 않을 때 발생하는 예외.

    Attributes:
        user_auth_type (AuthType): 사용자의 인증 타입 값.
    """

    def __init__(self, user_auth_type: AuthType) -> None:
        super().__init__(
            f"Only local auth type can change password, User type: {user_auth_type.value.value}"
        )
