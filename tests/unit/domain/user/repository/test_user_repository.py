from uuid import UUID

import pytest

from application.ports.repository.exceptions import EntityNotFoundError
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from domain.user.repository.user_repository import UserRepository
from tests.unit.conftest import FakeUserEntity


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
def repository(
    valid_user1: FakeUserEntity, valid_user2: FakeUserEntity
) -> FakeInMemoryUserRepository:
    items = {
        valid_user1.id: valid_user1,
        valid_user2.id: valid_user2,
    }
    return FakeInMemoryUserRepository(items=items)


class TestUserRepository:
    """
    FakeInMemoryUserRepository의 사용자명 및 이메일 중복 검사 테스트 클래스입니다.

    이 테스트 클래스는 저장소에서 사용자명과 이메일 중복 여부를 확인할 때,
    중복 시 예외가 제대로 발생하는지, 중복이 아닐 때는 예외 없이 통과하는지를 검증합니다.
    """

    def test_check_username_exists_raises_when_duplicate(
        self,
        repository: FakeInMemoryUserRepository,
        valid_user1: FakeUserEntity,
        valid_user2: FakeUserEntity,
    ):
        """
        중복된 사용자명에 대해 UsernameAlreadyExistsError 예외를 발생시키는지 확인합니다.

        Given: 저장소에 "test1", "test2" 사용자명이 존재할 때
        When: 해당 사용자명으로 중복 검사 메서드를 호출하면
        Then: UsernameAlreadyExistsError 예외가 발생해야 합니다.
        """
        with pytest.raises(UsernameAlreadyExistsError):
            repository.check_username_exists(valid_user1.username)
        with pytest.raises(UsernameAlreadyExistsError):
            repository.check_username_exists(valid_user2.username)

    def test_check_username_exists_non_existing(
        self, repository: FakeInMemoryUserRepository
    ):
        """
        존재하지 않는 사용자명에 대해서는 예외 없이 통과하는지 확인합니다.

        Given: 저장소에 없는 사용자명 "non_existing"이 있을 때
        When: 해당 사용자명으로 중복 검사 메서드를 호출하면
        Then: 아무 예외도 발생하지 않아야 합니다.
        """
        repository.check_username_exists("non_existing")

    def test_check_email_exists_raises_when_duplicate(
        self,
        repository: FakeInMemoryUserRepository,
        valid_user1: FakeUserEntity,
        valid_user2: FakeUserEntity,
    ):
        """
        중복된 이메일에 대해 EmailAlreadyExistsError 예외를 발생시키는지 확인합니다.

        Given: 저장소에 "test1@test.com", "test2@test.com" 이메일이 존재할 때
        When: 해당 이메일로 중복 검사 메서드를 호출하면
        Then: EmailAlreadyExistsError 예외가 발생해야 합니다.
        """
        with pytest.raises(EmailAlreadyExistsError):
            repository.check_email_exists(valid_user1.email)
        with pytest.raises(EmailAlreadyExistsError):
            repository.check_email_exists(valid_user2.email)

    def test_check_email_exists_non_existing(
        self, repository: FakeInMemoryUserRepository
    ):
        """
        존재하지 않는 이메일에 대해서는 예외 없이 통과하는지 확인합니다.

        Given: 저장소에 없는 이메일 "non_existing@test.com"이 있을 때
        When: 해당 이메일로 중복 검사 메서드를 호출하면
        Then: 아무 예외도 발생하지 않아야 합니다.
        """
        repository.check_email_exists("non_existing@test.com")
