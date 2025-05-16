"""도메인 사용자(User) 관련 유효성 검증 예외 정의 모듈입니다.

사용자 이름, 이메일, 비밀번호 등의 형식 및 제약 조건 위반 시 발생하는
도메인 특화 예외들을 정의합니다.
"""


class EmptyUsernameError(Exception):
    """사용자 이름이 비어 있는 경우 발생하는 예외입니다.

    사용자 이름은 공백이 아닌 유효한 문자열이어야 하며, 비어 있을 수 없습니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("사용자 이름은 비어 있을 수 없습니다.")


class UsernameTooLongError(Exception):
    """사용자 이름이 최대 길이 제한을 초과한 경우 발생하는 예외입니다.

    사용자 이름은 최대 50자까지만 허용됩니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("사용자 이름은 50자를 초과할 수 없습니다.")


class InvalidEmailFormatError(Exception):
    """이메일 주소의 형식이 유효하지 않은 경우 발생하는 예외입니다.

    '@'와 도메인 구문이 포함된 이메일 형식이어야 합니다.
    """

    def __init__(self) -> None:
        """기본 예외 메시지를 설정하여 초기화합니다."""
        super().__init__("유효하지 않은 이메일 형식입니다.")


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
