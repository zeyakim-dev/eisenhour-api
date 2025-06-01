from dataclasses import dataclass, field
from uuid import UUID, uuid4

import pytest

from domain.auth.auth_info.local.repository.exceptions import LocalAuthInfoNotFoundError
from domain.auth.auth_info.local.repository.local_auth_info_repository import (
    LocalAuthInfoRepository,
)


@dataclass(frozen=True, kw_only=True)
class LocalAuthInfo:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    hashed_password: str


class InMemoryLocalAuthInfoRepository(LocalAuthInfoRepository):
    def __init__(self, items: dict[UUID, LocalAuthInfo] | None = None):
        self.items = items or {}

    async def _save(self, entity: LocalAuthInfo) -> None:
        self.items[entity.id] = entity

    async def _get(self, id: UUID) -> LocalAuthInfo:
        return self.items.get(id)

    async def _delete(self, id: UUID) -> None:
        self.items.pop(id, None)

    async def _get_user_auth_info(self, user_id: UUID) -> LocalAuthInfo | None:
        return self.items.get(user_id)


@pytest.fixture
def test_user_id():
    return uuid4()


@pytest.fixture
def test_local_auth_info(test_user_id: UUID):
    return LocalAuthInfo(user_id=test_user_id, hashed_password="test_hashed_password")


@pytest.fixture
def local_auth_info_repository(test_local_auth_info: LocalAuthInfo):
    return InMemoryLocalAuthInfoRepository(
        items={test_local_auth_info.user_id: test_local_auth_info}
    )


@pytest.mark.unit
class TestLocalAuthInfoRepository:
    async def test_get_user_auth_info_success(
        self,
        local_auth_info_repository: InMemoryLocalAuthInfoRepository,
        test_local_auth_info,
    ):
        """get_user_auth_info가 존재하는 사용자 ID에서 LocalAuthInfo를 반환하는지 검증한다.

        Given:
            테스트용 LocalAuthInfo가 저장된 InMemoryLocalAuthInfoRepository.
        When:
            get_user_auth_info를 테스트용 user_id로 호출하면.
        Then:
            해당 LocalAuthInfo 인스턴스를 올바르게 반환해야 한다.
        """
        local_auth_info = await local_auth_info_repository.get_user_auth_info(
            test_local_auth_info.user_id
        )
        assert local_auth_info.user_id == test_local_auth_info.user_id
        assert local_auth_info.hashed_password == test_local_auth_info.hashed_password

    async def test_get_user_auth_info_not_found(
        self,
        local_auth_info_repository: InMemoryLocalAuthInfoRepository,
    ):
        """get_user_auth_info가 존재하지 않는 사용자 ID에서 EntityNotFoundError를 발생시키는지 검증한다.

        Given:
            LocalAuthInfo가 비어 있거나 해당 user_id가 없는 InMemoryLocalAuthInfoRepository.
        When:
            get_user_auth_info를 존재하지 않는 user_id로 호출하면.
        Then:
            EntityNotFoundError 예외를 발생시켜야 한다.
        """
        nonexisting_user_id = uuid4()
        with pytest.raises(LocalAuthInfoNotFoundError):
            await local_auth_info_repository.get_user_auth_info(nonexisting_user_id)
