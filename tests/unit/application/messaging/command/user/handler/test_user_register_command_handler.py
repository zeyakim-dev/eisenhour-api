from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

import pytest

from application.messaging.command.user.handler.user_register_command_handler import (
    UserRegisterCommandHandler,
)
from application.messaging.command.user.user_register_command import UserRegisterCommand
from application.ports.repository.exceptions import EntityNotFoundError
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from domain.user.repository.user_repository import UserRepository


@dataclass(frozen=True, kw_only=True)
class FakeUserEntity:
    id: UUID = field(default_factory=uuid4)
    username: str
    email: str
    password: str


class FakeInMemoryUserRepository(UserRepository):
    def __init__(self, items: dict[UUID, FakeUserEntity] | None = None):
        self.items = items or {}

    def _save(self, entity: FakeUserEntity) -> None:
        self.items[entity.id] = entity

    def _get(self, id: UUID) -> FakeUserEntity:
        try:
            return self.items[id]
        except KeyError:
            raise EntityNotFoundError(self.__class__.__name__, id)

    def _delete(self, id: UUID) -> None:
        try:
            del self.items[id]
        except KeyError:
            raise EntityNotFoundError(self.__class__.__name__, id)

    def _is_duplicate_username(self, username: str) -> bool:
        return any(user.username == username for user in self.items.values())

    def _is_duplicate_email(self, email: str) -> bool:
        return any(user.email == email for user in self.items.values())


@pytest.fixture
def fake_user_1() -> FakeUserEntity:
    return FakeUserEntity(username="test1", email="test1@test.com", password="test1")


@pytest.fixture
def fake_user_2() -> FakeUserEntity:
    return FakeUserEntity(username="test2", email="test2@test.com", password="test2")


@pytest.fixture
def repository(
    fake_user_1: FakeUserEntity, fake_user_2: FakeUserEntity
) -> FakeInMemoryUserRepository:
    items = {
        fake_user_1.id: fake_user_1,
        fake_user_2.id: fake_user_2,
    }
    return FakeInMemoryUserRepository(items=items)


class FakeTimeProvider:
    def now(self):
        return datetime.now()


class FakeHasher:
    def hash(self, password: str) -> str:
        return "hashed_" + password

    def verify(self, password: str, hashed_password: str) -> bool:
        return "hashed_" + password == hashed_password


@pytest.fixture
def time_provider():
    return FakeTimeProvider()


@pytest.fixture
def hasher():
    return FakeHasher()


@pytest.fixture
def user_register_command_handler(repository, time_provider, hasher):
    return UserRegisterCommandHandler(
        repository=repository, time_provider=time_provider, hasher=hasher
    )


class TestUserRegisterCommand:
    def test_successful_registration(
        self, user_register_command_handler, time_provider
    ):
        command = UserRegisterCommand.create(
            time_provider=time_provider,
            username="newuser",
            email="newuser@example.com",
            plain_password="Secret_123!",
        )

        result = user_register_command_handler.execute(command)
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"

    def test_duplicate_username_raises_error(
        self, user_register_command_handler, time_provider
    ):
        command = UserRegisterCommand.create(
            time_provider=time_provider,
            username="test1",  # 이미 등록된 username (fake_user_1)
            email="unique@example.com",
            plain_password="Secret_123!",
        )

        with pytest.raises(UsernameAlreadyExistsError):
            user_register_command_handler.execute(command)

    def test_duplicate_email_raises_error(
        self, user_register_command_handler, time_provider
    ):
        command = UserRegisterCommand.create(
            time_provider=time_provider,
            username="uniqueuser",
            email="test2@test.com",  # 이미 등록된 email (fake_user_2)
            plain_password="Secret_123!",
        )

        with pytest.raises(EmailAlreadyExistsError):
            user_register_command_handler.execute(command)
