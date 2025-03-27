from src.eisenhour_api.domain.entities.user.entities import User


class UserFactory:
    @staticmethod
    def create(username: str, email: str, hashed_password: str) -> User:
        return User(
            username=username,
            email=email,
            password=hashed_password
        )

