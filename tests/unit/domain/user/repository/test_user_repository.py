from uuid import UUID

import pytest
import pytest_asyncio

from application.ports.repository.exceptions import EntityNotFoundError
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
)
from domain.user.repository.user_repository import (
    UserRepository,  # AsyncRepository 상속
)
from tests.unit.conftest import FakeUserEntity


class FakeInMemoryAsyncUserRepository(UserRepository):
    """비동기 메모리 기반 UserRepository Fake 구현체."""

    def __init__(self, items: dict[UUID, FakeUserEntity] | None = None):
        self.items = items or {}

    async def _save(self, entity: FakeUserEntity) -> None:
        self.items[entity.id] = entity

    async def _get(self, id: UUID) -> FakeUserEntity:
        try:
            return self.items[id]
        except KeyError:
            raise EntityNotFoundError(self.__class__.__name__, id)

    async def _delete(self, id: UUID) -> None:
        if id not in self.items:
            raise EntityNotFoundError(self.__class__.__name__, id)
        del self.items[id]

    async def _get_by_username(self, username: str) -> FakeUserEntity | None:
        filtered_result = filter(lambda u: u.username == username, self.items.values())
        return next(filtered_result, None)

    async def _is_duplicate_email(self, email: str) -> bool:
        return any(u.email == email for u in self.items.values())


@pytest_asyncio.fixture
async def repository(valid_user1: FakeUserEntity, valid_user2: FakeUserEntity):
    """두 개의 사용자로 초기화된 비동기 저장소를 제공합니다."""
    items = {valid_user1.id: valid_user1, valid_user2.id: valid_user2}
    return FakeInMemoryAsyncUserRepository(items=items)


@pytest.mark.asyncio
class TestAsyncUserRepository:
    """UserRepository 중복 검사 및 조회 기능(비동기) 검증."""

    async def test_get_by_username_returns_user_when_exists(
        self, repository: FakeInMemoryAsyncUserRepository, valid_user1, valid_user2
    ):
        """
        Given: test1/test2가 저장소에 있을 때
        When: get_by_username() 호출
        Then: 해당 UserEntity가 반환된다
        """
        user = await repository.get_by_username(valid_user1.username)
        assert user is not None
        assert user.username == valid_user1.username
        user2 = await repository.get_by_username(valid_user2.username)
        assert user2 is not None
        assert user2.username == valid_user2.username

    async def test_get_by_username_returns_none_when_not_exists(self, repository):
        """
        Given: 저장소에 없는 이름
        When: get_by_username() 호출
        Then: None이 반환된다
        """
        user = await repository.get_by_username("nonexistent")
        assert user is None

    async def test_check_email_exists_raises_when_duplicate(
        self, repository, valid_user1, valid_user2
    ):
        """
        Given: test1@test.com/test2@test.com이 있을 때
        When: check_email_exists() 호출
        Then: EmailAlreadyExistsError 발생
        """
        with pytest.raises(EmailAlreadyExistsError):
            await repository.check_email_exists(valid_user1.email)
        with pytest.raises(EmailAlreadyExistsError):
            await repository.check_email_exists(valid_user2.email)

    async def test_check_email_exists_non_existing(self, repository):
        """
        Given: 저장소에 없는 이메일
        When: check_email_exists() 호출
        Then: 예외 없이 정상 반환
        """
        await repository.check_email_exists("nope@example.com")
