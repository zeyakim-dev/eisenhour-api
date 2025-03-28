import pytest

from src.eisenhour_api.domain.repositories.user_repository import UserRepository
from tests.unit.domain.conftest import FakeUserDomain


class TestUserRepository:
    def test_create(self, user_repository: UserRepository, new_user_domain: FakeUserDomain):
        user_repository.create(new_user_domain)
        assert user_repository.read(new_user_domain.id) == new_user_domain

    def test_read(self, user_repository: UserRepository, existing_user_domain: FakeUserDomain):
        user = user_repository.read(existing_user_domain.id)
        assert user == existing_user_domain

    def test_read_by_username(self, user_repository: UserRepository, existing_user_domain: FakeUserDomain):
        user = user_repository.read_by_username(existing_user_domain.username)
        assert user == existing_user_domain

    def test_read_by_username_not_found(self, user_repository: UserRepository):
        with pytest.raises(ValueError):
            user_repository.read_by_username("non_existent_username")

    def test_update(self, user_repository: UserRepository, existing_user_domain: FakeUserDomain):
        updated_user_domain = FakeUserDomain(
            id=existing_user_domain.id,
            username="updated",
            email=existing_user_domain.email,
            password=existing_user_domain.password
        )
        user_repository.update(updated_user_domain)
        assert user_repository.users[existing_user_domain.id].username == "updated"

    def test_delete(self, user_repository: UserRepository, existing_user_domain: FakeUserDomain):
        user_repository.delete(existing_user_domain.id)
        assert existing_user_domain.id not in user_repository.users

    