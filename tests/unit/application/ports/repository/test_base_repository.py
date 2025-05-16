from dataclasses import dataclass, field
from uuid import UUID, uuid4

import pytest

from application.ports.repository.exceptions import EntityNotFoundError
from application.ports.repository.repository import Repository
from domain.base.entity import Entity


@dataclass(frozen=True, kw_only=True)
class FakeUserEntity:
    id: UUID = field(default_factory=uuid4)
    username: str
    email: str
    password: str


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
def fake_user_1() -> FakeUserEntity:
    return FakeUserEntity(username="test1", email="test1@test.com", password="test1")


@pytest.fixture
def fake_user_2() -> FakeUserEntity:
    return FakeUserEntity(username="test2", email="test2@test.com", password="test2")


@pytest.fixture
def repository(
    fake_user_1: FakeUserEntity, fake_user_2: FakeUserEntity
) -> FakeInMemoryRepository:
    items = {
        fake_user_1.id: fake_user_1,
        fake_user_2.id: fake_user_2,
    }
    return FakeInMemoryRepository(items=items)


class TestBaseRepository:
    def test_save_new_entity(self, repository: FakeInMemoryRepository):
        user = FakeUserEntity(
            username="test2", email="test2@test.com", password="test2"
        )
        repository.save(user)
        assert user.id in repository.items
        assert repository.items[user.id] == user

    def test_save_existing_entity_overwrites_data(
        self, repository: FakeInMemoryRepository, fake_user_1: FakeUserEntity
    ):
        new_password = "new_password"
        changed_entity = FakeUserEntity(
            id=fake_user_1.id,
            username=fake_user_1.username,
            email=fake_user_1.email,
            password=new_password,
        )
        repository.save(changed_entity)

        assert changed_entity.id in repository.items
        assert repository.items.get(changed_entity.id).password == new_password

    def test_get_success(
        self, repository: FakeInMemoryRepository, fake_user_1: FakeUserEntity
    ):
        assert repository.get(fake_user_1.id) == fake_user_1

    def test_get_non_existing_entity(self, repository: FakeInMemoryRepository):
        non_existing_id = uuid4()
        with pytest.raises(EntityNotFoundError):
            repository.get(non_existing_id)

    def test_delete(
        self, repository: FakeInMemoryRepository, fake_user_2: FakeUserEntity
    ):
        repository.delete(fake_user_2.id)
        assert fake_user_2.id not in repository.items

    def test_delete_non_existing_entity(self, repository: FakeInMemoryRepository):
        non_existing_id = uuid4()
        with pytest.raises(EntityNotFoundError):
            repository.delete(non_existing_id)
