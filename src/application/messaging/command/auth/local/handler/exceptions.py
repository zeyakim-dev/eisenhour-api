class UsernameAlreadyExistsError(Exception):
    """이미 존재하는 사용자 이름에 대한 예외입니다.

    사용자 등록 또는 수정 과정에서 중복된 사용자 이름이 감지될 경우 발생합니다.
    """

    def __init__(self, username: str):
        """예외 메시지를 설정하여 초기화합니다.

        Args:
            username (str): 중복된 사용자 이름.
        """
        super().__init__(f"Username {username} already exists")


class WrongPasswordError(Exception):
    """잘못된 비밀번호에 대한 예외입니다.

    사용자 인증 과정에서 입력된 비밀번호가 저장된 비밀번호와 일치하지 않을 경우 발생합니다.
    """

    def __init__(self, username: str):
        """예외 메시지를 설정하여 초기화합니다.

        Args:
            username (str): 인증을 시도한 사용자 이름.
        """
        super().__init__(f"Wrong password for user {username}")
