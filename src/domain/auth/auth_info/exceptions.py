from domain.auth.auth_info.value_objects import AuthType


class InvalidAuthTypeError(Exception):
    def __init__(self, auth_type: AuthType) -> None:
        super().__init__(f"Invalid auth type: {auth_type.value.value}")
