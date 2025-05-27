from uuid import UUID

from domain.auth.auth_info.base.value_objects import AuthType


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


class PasswordTooShortError(Exception):
    """비밀번호 길이가 최소 길이 미만인 경우 발생하는 예외입니다.

    비밀번호는 최소 8자 이상이어야 합니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("비밀번호는 최소 8자 이상이어야 합니다.")


class PasswordTooLongError(Exception):
    """비밀번호 길이가 최대 길이를 초과한 경우 발생하는 예외입니다.

    비밀번호는 최대 100자까지만 허용됩니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("비밀번호는 최대 100자를 초과할 수 없습니다.")


class PasswordMissingUppercaseError(Exception):
    """비밀번호에 대문자가 포함되지 않은 경우 발생하는 예외입니다.

    최소 하나 이상의 대문자가 포함되어야 합니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("비밀번호에는 최소 하나의 대문자가 포함되어야 합니다.")


class PasswordMissingLowercaseError(Exception):
    """비밀번호에 소문자가 포함되지 않은 경우 발생하는 예외입니다.

    최소 하나 이상의 소문자가 포함되어야 합니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("비밀번호에는 최소 하나의 소문자가 포함되어야 합니다.")


class PasswordMissingNumberError(Exception):
    """비밀번호에 숫자가 포함되지 않은 경우 발생하는 예외입니다.

    최소 하나 이상의 숫자가 포함되어야 합니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("비밀번호에는 최소 하나의 숫자가 포함되어야 합니다.")


class PasswordMissingSpecialCharacterError(Exception):
    """비밀번호에 특수문자가 포함되지 않은 경우 발생하는 예외입니다.

    최소 하나 이상의 특수문자(!@#$ 등)가 포함되어야 합니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("비밀번호에는 최소 하나의 특수문자가 포함되어야 합니다.")
