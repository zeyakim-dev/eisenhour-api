from dataclasses import dataclass, field
from uuid import UUID, uuid4

import pytest

from application.ports.repository.exceptions import EntityNotFoundError
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from domain.user.repository.user_repository import UserRepository
from domain.user.user import User


@dataclass(frozen=True, kw_only=True)
class FakeUserEntity:
    id: UUID = field(default_factory=uuid4)
    username: str
    email: str
    password: str


class FakeInMemoryUserRepository(UserRepository):
    def __init__(self, items: dict[UUID, User] | None = None):
        self.items = items or {}

    def _save(self, entity: User) -> None:
        self.items[entity.id] = entity

    def _get(self, id: UUID) -> User:
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


class TestUserRepository:
    def test_check_username_exists(self, repository: FakeInMemoryUserRepository):
        with pytest.raises(UsernameAlreadyExistsError):
            repository.check_username_exists("test1")
        with pytest.raises(UsernameAlreadyExistsError):
            repository.check_username_exists("test2")

    def test_check_username_exists_non_existing(
        self, repository: FakeInMemoryUserRepository
    ):
        repository.check_username_exists("non_existing")

    def test_check_email_exists(self, repository: FakeInMemoryUserRepository):
        with pytest.raises(EmailAlreadyExistsError):
            repository.check_email_exists("test1@test.com")
        with pytest.raises(EmailAlreadyExistsError):
            repository.check_email_exists("test2@test.com")

    def test_check_email_exists_non_existing(
        self, repository: FakeInMemoryUserRepository
    ):
        repository.check_email_exists("non_existing@test.com")
