class LocalAuthInfoNotFoundError(Exception):
    """지정한 LocalAuthInfo가 존재하지 않을 때 발생하는 예외."""

    def __init__(self, user_id: str) -> None:
        super().__init__(f"LocalAuthInfo not found for user_id: {user_id}")
