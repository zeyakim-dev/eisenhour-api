class EmailAlreadyExistsError(Exception):
    """이미 존재하는 이메일 주소에 대한 예외입니다.

    사용자 등록 또는 수정 과정에서 중복된 이메일이 감지될 경우 발생합니다.
    """

    def __init__(self, email: str):
        """예외 메시지를 설정하여 초기화합니다.

        Args:
            email (str): 중복된 이메일 주소.
        """
        super().__init__(f"Email {email} already exists")


class UsernameNotFoundError(Exception):
    """Username not found error"""

    def __init__(self, username: str):
        super().__init__(f"Username {username} not found")
