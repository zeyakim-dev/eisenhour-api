class EmptyUsernameError(Exception):
    def __init__(self) -> None:
        super().__init__("사용자 이름은 비어 있을 수 없습니다.")


class UsernameTooLongError(Exception):
    def __init__(self) -> None:
        super().__init__("사용자 이름은 50자를 초과할 수 없습니다.")


class InvalidEmailFormatError(Exception):
    def __init__(self) -> None:
        super().__init__("유효하지 않은 이메일 형식입니다.")


class PasswordTooShortError(Exception):
    def __init__(self) -> None:
        super().__init__("비밀번호는 최소 8자 이상이어야 합니다.")


class PasswordTooLongError(Exception):
    def __init__(self) -> None:
        super().__init__("비밀번호는 최대 100자를 초과할 수 없습니다.")


class PasswordMissingUppercaseError(Exception):
    def __init__(self) -> None:
        super().__init__("비밀번호에는 최소 하나의 대문자가 포함되어야 합니다.")


class PasswordMissingLowercaseError(Exception):
    def __init__(self) -> None:
        super().__init__("비밀번호에는 최소 하나의 소문자가 포함되어야 합니다.")


class PasswordMissingNumberError(Exception):
    def __init__(self) -> None:
        super().__init__("비밀번호에는 최소 하나의 숫자가 포함되어야 합니다.")


class PasswordMissingSpecialCharacterError(Exception):
    def __init__(self) -> None:
        super().__init__("비밀번호에는 최소 하나의 특수문자가 포함되어야 합니다.")
