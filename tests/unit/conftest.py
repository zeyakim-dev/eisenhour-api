from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest

from application.ports.repository.exceptions import EntityNotFoundError
from domain.auth.auth_info.base.value_objects import AuthTypeEnum
from domain.auth.auth_info.local.value_objects import HashedPassword
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
)
from domain.user.value_objects import Email, Username


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
    updated_at: datetime = field(default_factory=datetime.now)
    username: Username
    email: Email


@pytest.fixture
def valid_user1():
    return FakeUserEntity(
        username=Username("test_user1"), email=Email("test1@example.com")
    )


@pytest.fixture
def valid_user2():
    return FakeUserEntity(
        username=Username("test_user2"), email=Email("test2@example.com")
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

    async def get_by_username(self, username: str) -> FakeUserEntity | None:
        filtered_result = filter(
            lambda u: u.username.value == username, self.items.values()
        )
        return next(filtered_result, None)

    async def check_email_exists(self, email: str) -> None:
        if any(u.email == email for u in self.items.values()):
            raise EmailAlreadyExistsError(email)


@pytest.fixture
def fake_user_inmemory_repository(
    valid_user1: FakeUserEntity, valid_user2: FakeUserEntity
):
    items = {valid_user1.id: valid_user1, valid_user2.id: valid_user2}
    return FakeInMemoryAsyncUserRepository(items=items)


@dataclass(frozen=True, kw_only=True)
class FakeLocalAuthInfoEntity:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    auth_type: str
    hashed_password: HashedPassword
    password_expired_at: datetime


class FakeInMemoryAsyncLocalAuthInfoRepository:
    """비동기 메모리 기반 LocalAuthInfoRepository Fake 구현체."""

    def __init__(self, items: dict[UUID, FakeUserEntity] | None = None):
        self.items = items or {}

    async def save(self, entity: FakeLocalAuthInfoEntity) -> None:
        self.items[entity.id] = entity

    async def get_user_auth_info(self, user_id: UUID):
        return next(
            filter(
                lambda local_auth_info: local_auth_info.user_id == user_id,
                self.items.values(),
            ),
            None,
        )


@pytest.fixture
def valid_local_auth_info1(valid_user1: FakeUserEntity):
    return FakeLocalAuthInfoEntity(
        user_id=valid_user1.id,
        auth_type=AuthTypeEnum.LOCAL.value,
        hashed_password=HashedPassword("hashed_Test_pw_1!"),
        password_expired_at=datetime.now() + timedelta(days=30),
    )


@pytest.fixture
def valid_local_auth_info2(valid_user2: FakeUserEntity):
    return FakeLocalAuthInfoEntity(
        user_id=valid_user2.id,
        auth_type=AuthTypeEnum.LOCAL.value,
        hashed_password=HashedPassword("hashed_Test_pw_2!"),
        password_expired_at=datetime.now() + timedelta(days=30),
    )


@pytest.fixture
def fake_local_auth_info_inmemory_repository(
    valid_local_auth_info1: FakeLocalAuthInfoEntity,
    valid_local_auth_info2: FakeLocalAuthInfoEntity,
):
    items = {
        valid_local_auth_info1.id: valid_local_auth_info1,
        valid_local_auth_info2.id: valid_local_auth_info2,
    }
    return FakeInMemoryAsyncLocalAuthInfoRepository(items=items)
