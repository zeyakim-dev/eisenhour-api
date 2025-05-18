from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

import pytest

from application.ports.repository.exceptions import EntityNotFoundError
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)


class FakeTimeProvider:
    def __init__(self) -> None:
        pass

    def now(self):
        return datetime.now()


@pytest.fixture
def time_provider():
    return FakeTimeProvider()


class FakeHasher:
    def hash(self, password: str) -> str:
        return "hashed_" + password

    def verify(self, password: str, hashed_password: str) -> bool:
        return "hashed_" + password == hashed_password


@pytest.fixture
def hasher():
    return FakeHasher()


@dataclass(frozen=True, kw_only=True)
class FakeUserEntity:
    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(default_factory=datetime.now)
    username: str
    email: str
    password: str


@pytest.fixture
def valid_user1():
    return FakeUserEntity(
        username="test_user1", email="test1@example.com", password="hashed_Test_pw_1!"
    )


@pytest.fixture
def valid_user2():
    return FakeUserEntity(
        username="test_user2", email="test2@example.com", password="hashed_Test_pw_2!"
    )


class FakeInMemoryAsyncUserRepository:
    """비동기 메모리 기반 UserRepository Fake 구현체."""

    def __init__(self, items: dict[UUID, FakeUserEntity] | None = None):
        self.items = items or {}

    async def save(self, entity: FakeUserEntity) -> None:
        self.items[entity.id] = entity

    async def get(self, id: UUID) -> FakeUserEntity:
        try:
            return self.items[id]
        except KeyError:
            raise EntityNotFoundError(self.__class__.__name__, id)

    async def delete(self, id: UUID) -> None:
        if id not in self.items:
            raise EntityNotFoundError(self.__class__.__name__, id)
        del self.items[id]

    async def check_username_exists(self, username: str) -> None:
        if any(u.username == username for u in self.items.values()):
            raise UsernameAlreadyExistsError(username)

    async def check_email_exists(self, email: str) -> None:
        if any(u.email == email for u in self.items.values()):
            raise EmailAlreadyExistsError(email)


@pytest.fixture
def fake_user_inmemory_repository(
    valid_user1: FakeUserEntity, valid_user2: FakeUserEntity
):
    items = {valid_user1.id: valid_user1, valid_user2.id: valid_user2}
    return FakeInMemoryAsyncUserRepository(items=items)
