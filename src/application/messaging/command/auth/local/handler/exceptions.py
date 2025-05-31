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
