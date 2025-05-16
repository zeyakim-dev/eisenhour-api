from uuid import UUID, uuid4

import pytest

from application.ports.repository.exceptions import EntityNotFoundError
from application.ports.repository.repository import Repository
from domain.base.entity import Entity
from tests.unit.conftest import FakeUserEntity


class FakeInMemoryRepository(Repository):
    def __init__(self, items: dict[UUID, Entity] | None = None):
        self.items = items or {}

    def _save(self, entity: Entity) -> None:
        self.items[entity.id] = entity

    def _get(self, id: UUID) -> Entity:
        try:
            return self.items[id]
        except KeyError:
            raise EntityNotFoundError(self.__class__.__name__, id)

    def _delete(self, id: UUID) -> None:
        try:
            del self.items[id]
        except KeyError:
            raise EntityNotFoundError(self.__class__.__name__, id)


@pytest.fixture
def repository(valid_user1, valid_user2) -> FakeInMemoryRepository:
    items = {
        valid_user1.id: valid_user1,
        valid_user2.id: valid_user2,
    }
    return FakeInMemoryRepository(items=items)


class TestBaseRepository:
    def test_save_new_entity(self, repository: FakeInMemoryRepository):
        new_user = FakeUserEntity(
            username="test2", email="test2@test.com", password="test2"
        )
        repository.save(new_user)
        assert new_user.id in repository.items
        assert repository.items[new_user.id] == new_user

    def test_save_existing_entity_overwrites_data(
        self, repository: FakeInMemoryRepository, valid_user1: FakeUserEntity
    ):
        new_password = "new_password"
        changed_entity = FakeUserEntity(
            id=valid_user1.id,
            username=valid_user1.username,
            email=valid_user1.email,
            password=new_password,
        )
        repository.save(changed_entity)

        assert changed_entity.id in repository.items
        assert repository.items.get(changed_entity.id).password == new_password

    def test_get_success(
        self, repository: FakeInMemoryRepository, valid_user1: FakeUserEntity
    ):
        assert repository.get(valid_user1.id) == valid_user1

    def test_get_non_existing_entity(self, repository: FakeInMemoryRepository):
        non_existing_id = uuid4()
        with pytest.raises(EntityNotFoundError):
            repository.get(non_existing_id)

    def test_delete(
        self, repository: FakeInMemoryRepository, valid_user2: FakeUserEntity
    ):
        repository.delete(valid_user2.id)
        assert valid_user2.id not in repository.items

    def test_delete_non_existing_entity(self, repository: FakeInMemoryRepository):
        non_existing_id = uuid4()
        with pytest.raises(EntityNotFoundError):
            repository.delete(non_existing_id)
