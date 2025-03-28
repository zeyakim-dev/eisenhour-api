from typing import Protocol
from src.eisenhour_api.domain.entities.user.entities import User, UserFactory
from src.eisenhour_api.domain.repositories.user_repository import UserRepository


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        ...
    
    def verify(self, password: str, hashed_password: str) -> bool:
        ...


class CreateUserRequest(Protocol):
    username: str
    email: str
    password: str


class LoginUserRequest(Protocol):
    username: str
    password: str


class UserService:
    def __init__(self, user_factory: UserFactory, user_repository: UserRepository):
        self.user_factory = user_factory
        self.user_repository = user_repository

    def register(self, user_data: CreateUserRequest, password_hasher: PasswordHasher) -> User:
        hashed_password = password_hasher.hash(user_data.password)
        new_user = self.user_factory.create(user_data.username, user_data.email, hashed_password)
        self.user_repository.create(new_user)

        return new_user
    
    def login(self, user_data: LoginUserRequest, password_hasher: PasswordHasher) -> None:
        user = self.user_repository.read_by_username(user_data.username)
        if not password_hasher.verify(user_data.password, user.password):
            raise ValueError("Invalid password")
