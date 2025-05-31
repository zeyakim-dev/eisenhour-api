from uuid import UUID, uuid4

import pytest

from domain.auth.auth_info.google.google_auth_info import GoogleAuthInfo
from domain.auth.auth_info.google.repository.google_auth_info_repository import (
    GoogleAuthInfoRepository,
)
from domain.auth.auth_info.google.value_objects import GoogleSub


class InMemoryGoogleAuthInfoRepository(GoogleAuthInfoRepository):
    def __init__(self, items: dict[UUID, GoogleAuthInfo] | None = None):
        self.items = items or {}

    async def _save(self, entity: GoogleAuthInfo) -> None:
        self.items[entity.id] = entity

    async def _get(self, id):
        return self.items.get(id)

    async def _delete(self, id):
        self.items.pop(id, None)

    async def _get_auth_info_by_sub(self, sub: GoogleSub) -> GoogleAuthInfo | None:
        filtered_items = (item for item in self.items.values() if item.sub == sub)
        return next(filtered_items, None)


@pytest.fixture
def test_sub():
    return GoogleSub("test-google-sub")


@pytest.fixture
def test_google_auth_info(test_sub):
    return GoogleAuthInfo.create(
        now=None,
        user_id=uuid4(),
        sub=test_sub,
        avatar_url="https://example.com/avatar.png",
    )


@pytest.fixture
def google_auth_info_repository(test_google_auth_info):
    return InMemoryGoogleAuthInfoRepository(
        items={test_google_auth_info.id: test_google_auth_info}
    )


@pytest.mark.unit
@pytest.mark.asyncio
class TestGoogleAuthInfoRepository:
    async def test_get_auth_info_by_sub_success(
        self, google_auth_info_repository, test_google_auth_info, test_sub
    ):
        """
        GoogleSub로 인증 정보를 조회할 때 정상적으로 반환되는지 검증합니다.

        Given: 저장소에 GoogleAuthInfo가 저장되어 있을 때
        When: get_auth_info_by_sub를 해당 sub로 호출하면
        Then: 해당 GoogleAuthInfo 인스턴스를 반환해야 한다.
        """
        result = await google_auth_info_repository.get_auth_info_by_sub(test_sub)
        assert result == test_google_auth_info

    async def test_get_auth_info_by_sub_not_found(self, google_auth_info_repository):
        """
        존재하지 않는 sub로 조회 시 None을 반환하는지 검증합니다.

        Given: 저장소에 해당 sub가 없을 때
        When: get_auth_info_by_sub를 호출하면
        Then: None을 반환해야 한다.
        """
        nonexisting_sub = GoogleSub("nonexisting-sub")
        result = await google_auth_info_repository.get_auth_info_by_sub(nonexisting_sub)
        assert result is None
