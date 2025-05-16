class UsernameAlreadyExistsError(Exception):
    def __init__(self, username: str):
        super().__init__(f"Username {username} already exists")


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        super().__init__(f"Email {email} already exists")
