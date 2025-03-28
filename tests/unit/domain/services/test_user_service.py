import pytest
from uuid import UUID, uuid4

from src.eisenhour_api.domain.services.user_service import UserService


class FakeCreateUserRequest:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password


class FakeLoginUserRequest:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class FakePasswordHasher:
    def hash(self, password: str) -> str:
        return f"hashed_{password}"
    
    def verify(self, password: str, hashed_password: str) -> bool:
        return f"hashed_{password}" == hashed_password


class FakeUserDomain:
    def __init__(self, id: UUID, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password


class FakeUserFactory:
    def create(self, username: str, email: str, hashed_password: str) -> FakeUserDomain:
        return FakeUserDomain(
            id=uuid4(),
            username=username,
            email=email,
            password=hashed_password)

@pytest.fixture
def password_hasher():
    return FakePasswordHasher()

@pytest.fixture
def user_factory():
    return FakeUserFactory()


@pytest.fixture
def user_service(user_factory, user_repository):
    return UserService(user_factory, user_repository)


class TestUserService:
    def test_register_user(self, user_service, password_hasher):
        # Given
        user_data = FakeCreateUserRequest(
            username="test_user",
            email="test@example.com",
            password="password123"
        )
        
        # When
        created_user = user_service.register(user_data, password_hasher)
        
        # Then
        assert created_user.username == user_data.username
        assert created_user.email == user_data.email

    def test_login_success(self, user_service, password_hasher, existing_user_domain):
        # Given
        login_data = FakeLoginUserRequest(
            username=existing_user_domain.username,
            password="existing_user_password"
        )

        user_service.login(login_data, password_hasher)

    def test_login_invalid_password(self, user_service, existing_user_domain, password_hasher):
        # Given
        login_data = FakeLoginUserRequest(
            username=existing_user_domain.username,
            password="wrong_password"
        )

        # When/Then
        with pytest.raises(ValueError, match="Invalid password"):
            user_service.login(login_data, password_hasher)

    def test_login_nonexistent_user(self, user_service, user_repository, password_hasher):
        # Given

        login_data = FakeLoginUserRequest(
            username="nonexistent",
            password="password123"
        )
        
        # When/Then
        with pytest.raises(ValueError, match="User not found"):
            user_service.login(login_data, password_hasher) 