from typing import Protocol
from eisenhour_api.domain.entities.user.entities import User
from eisenhour_api.domain.repositories.user_repository import UserRepository


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
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, user_data: CreateUserRequest, password_hasher: PasswordHasher) -> None:
        hashed_password = password_hasher.hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )
        self.user_repository.create(user)
    
    def login(self, user_data: LoginUserRequest, password_hasher: PasswordHasher) -> None:
        user = self.user_repository.read_by_username(user_data.username)
        if not password_hasher.verify(user_data.password, user.password):
            raise ValueError("Invalid password")
