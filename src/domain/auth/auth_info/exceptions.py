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
