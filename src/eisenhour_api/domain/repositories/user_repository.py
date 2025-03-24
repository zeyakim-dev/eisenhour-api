from datetime import datetime
from typing import Protocol
from uuid import UUID
from eisenhour_api.domain.entities.user.entities import User


class UserModel(Protocol):
    id: UUID
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


class UserMapper(Protocol):
    def to_entity(self, model: UserModel) -> User:
        ...
    
    def to_model(self, user: User) -> UserModel:
        ...


class UserRepository:
    def __init__(self, mapper: UserMapper):
        self.mapper = mapper

    def create(self, user: User) -> None:
        user_model = self.mapper.to_model(user)
        self._create(user_model)
    
    def _create(self, user_model: UserModel) -> None:
        ...
    
    def read(self, user_id: UUID) -> User:
        user_model = self._read(user_id)
        if not user_model:
            raise ValueError("User not found")
        return self.mapper.to_entity(user_model)

    def _read(self, user_id: UUID) -> UserModel:
        ...
    
    def read_by_username(self, username: str) -> User:
        user_model = self._read_by_username(username)
        if not user_model:
            raise ValueError("User not found")
        return self.mapper.to_entity(user_model)

    def _read_by_username(self, username: str) -> UserModel:
        ...

    def update(self, user: User) -> None:
        user_model = self.mapper.to_model(user)
        self._update(user_model)

    def _update(self, user_model: UserModel) -> None:
        ...

    def delete(self, user_id: UUID) -> None:
        self._delete(user_id)

    def _delete(self, user_id: UUID) -> None:
        ...