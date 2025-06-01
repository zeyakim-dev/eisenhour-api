from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from application.ports.repository.exceptions import EntityNotFoundError
from application.ports.repository.repository import AsyncRepository
from domain.base.entity import Entity
from domain.user.value_objects import Email, Username
from tests.unit.conftest import FakeUserEntity


class FakeInMemoryAsyncRepository(AsyncRepository[Entity]):
    """비동기 메모리 기반 저장소의 Fake 구현체입니다.

    비동기 환경에서 테스트용으로 엔티티 저장, 조회, 삭제 기능을 제공합니다.
    """

    def __init__(self, items: dict[UUID, Entity] | None = None):
        """옵션으로 주어진 항목 맵으로 저장소를 초기화합니다."""
        self.items = items or {}

    async def _save(self, entity: Entity) -> None:
        """엔티티를 메모리에 저장 또는 갱신합니다."""
        self.items[entity.id] = entity

    async def _get(self, id: UUID) -> Entity:
        """ID로 엔티티를 조회하고, 없으면 예외를 발생시킵니다."""
        try:
            return self.items[id]
        except KeyError:
            raise EntityNotFoundError(self.__class__.__name__, id)

    async def _delete(self, id: UUID) -> None:
        """ID로 엔티티를 삭제하고, 없으면 예외를 발생시킵니다."""
        try:
            del self.items[id]
        except KeyError:
            raise EntityNotFoundError(self.__class__.__name__, id)


@pytest_asyncio.fixture
async def repository(
    valid_user1: FakeUserEntity, valid_user2: FakeUserEntity
) -> FakeInMemoryAsyncRepository:
    """두 개의 사용자 엔티티로 초기화된 비동기 저장소를 제공합니다."""
    items = {valid_user1.id: valid_user1, valid_user2.id: valid_user2}
    return FakeInMemoryAsyncRepository(items=items)


@pytest.mark.asyncio
class TestAsyncRepository:
    async def test_save_new_entity(self, repository: FakeInMemoryAsyncRepository):
        """저장소에 새로운 엔티티를 저장한다.

        Given: 저장소가 빈 상태이고 새로운 엔티티를 준비했을 때
        When: save()를 호출하면
        Then: repository.items에 엔티티가 추가되고 동일 객체가 반환된다
        """
        new_user = FakeUserEntity(
            username=Username("test2"),
            email=Email("test2@test.com"),
        )
        await repository.save(new_user)
        assert new_user.id in repository.items
        assert repository.items[new_user.id] == new_user

    async def test_save_existing_entity_overwrites_data(
        self, repository: FakeInMemoryAsyncRepository, valid_user1: FakeUserEntity
    ):
        """기존 엔티티를 덮어쓴다.

        Given: valid_user1이 저장소에 있고 동일한 ID를 가진 변경된 엔티티가 준비되었을 때
        When: save()를 호출하면
        Then: repository.items의 엔티티가 새 인스턴스로 업데이트된다
        """
        changed_entity = FakeUserEntity(
            id=valid_user1.id,
            username=valid_user1.username.value,
            email=valid_user1.email.value,
        )
        await repository.save(changed_entity)
        assert changed_entity.id in repository.items
        assert (
            repository.items[changed_entity.id].username == valid_user1.username.value
        )
        assert repository.items[changed_entity.id].email == valid_user1.email.value

    async def test_get_success(
        self, repository: FakeInMemoryAsyncRepository, valid_user1: FakeUserEntity
    ):
        """엔티티 조회가 성공한다.

        Given: valid_user1이 저장소에 있을 때
        When: get()를 호출하면
        Then: valid_user1 인스턴스가 반환된다
        """
        result = await repository.get(valid_user1.id)
        assert result == valid_user1

    async def test_get_non_existing_entity_raises(
        self, repository: FakeInMemoryAsyncRepository
    ):
        """존재하지 않는 엔티티 조회 시 예외를 발생시킨다.

        Given: repository.items에 없는 ID가 있을 때
        When: get()를 호출하면
        Then: EntityNotFoundError 예외가 발생한다
        """
        non_existing_id = uuid4()
        with pytest.raises(EntityNotFoundError):
            await repository.get(non_existing_id)

    async def test_delete_entity(
        self, repository: FakeInMemoryAsyncRepository, valid_user2: FakeUserEntity
    ):
        """엔티티 삭제가 성공한다.

        Given: valid_user2가 저장소에 있을 때
        When: delete()를 호출하면
        Then: repository.items에서 해당 엔티티가 제거된다
        """
        await repository.delete(valid_user2.id)
        assert valid_user2.id not in repository.items

    async def test_delete_non_existing_entity_raises(
        self, repository: FakeInMemoryAsyncRepository
    ):
        """존재하지 않는 엔티티 삭제 시 예외를 발생시킨다.

        Given: repository.items에 없는 ID가 있을 때
        When: delete()를 호출하면
        Then: EntityNotFoundError 예외가 발생한다
        """
        non_existing_id = uuid4()
        with pytest.raises(EntityNotFoundError):
            await repository.delete(non_existing_id)
