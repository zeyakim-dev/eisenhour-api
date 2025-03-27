from dataclasses import dataclass
from uuid import UUID, uuid4

import pytest

from src.eisenhour_api.domain.repositories.user_repository import UserRepository


@dataclass(frozen=True, kw_only=True)
class FakeUserDomain:
    id: UUID
    username: str
    email: str
    password: str


@dataclass(frozen=True, kw_only=True)
class FakeUserModel:
    id: UUID
    username: str
    email: str
    password: str


class FakeUserMapper:
    def to_entity(self, model: FakeUserModel) -> FakeUserDomain:
        return FakeUserDomain(
            id=model.id,
            username=model.username,
            email=model.email,
            password=model.password,
        )

    def to_model(self, user: FakeUserDomain) -> FakeUserModel:
        return FakeUserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
        )

class FakeUserRepository(UserRepository):
    def __init__(self, mapper: FakeUserMapper):
        self.mapper = mapper
        self.users: dict[UUID, FakeUserModel] = {}

    def _create(self, user_model: FakeUserModel) -> None:
        self.users[user_model.id] = user_model

    def _read(self, user_id: UUID) -> FakeUserModel | None:
        return self.users.get(user_id)

    def _read_by_username(self, username: str) -> FakeUserModel | None:
        stmt = filter(lambda user: user.username == username, self.users.values())
        return next(stmt, None)

    def _update(self, user_model: FakeUserModel) -> None:
        self.users[user_model.id] = user_model

    def _delete(self, user_id: UUID) -> None:
        self.users.pop(user_id, None)


@pytest.fixture
def existing_user_domain() -> FakeUserDomain:
    return FakeUserDomain(
        id=uuid4(),
        username="existing_user",
        email="existing_user@example.com",
        password="hashed_existing_user_password",
    )


@pytest.fixture
def new_user_domain() -> FakeUserDomain:
    return FakeUserDomain(
        id=uuid4(),
        username="new_user",
        email="new_user@example.com",
        password="hashed_new_user_password",
    )


@pytest.fixture
def user_repository(existing_user_domain: FakeUserDomain) -> UserRepository:
    repository = FakeUserRepository(FakeUserMapper())
    repository.users[existing_user_domain.id] = existing_user_domain

    return repository