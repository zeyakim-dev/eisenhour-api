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


class FakeUserRepository:
    def __init__(self):
        self.users: dict[UUID, FakeUserDomain] = {}
    



@pytest.fixture
def password_hasher():
    return FakePasswordHasher()


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)


class TestUserService:
    def test_register_user(self, user_service, user_repository, password_hasher):
        # Given
        user_data = FakeCreateUserRequest(
            username="test_user",
            email="test@example.com",
            password="password123"
        )
        
        # When
        user_service.register(user_data, password_hasher)
        
        # Then
        user_repository.create_user.assert_called_once()
        created_user = user_repository.create_user.call_args[0][0]
        assert created_user.username == user_data.username
        assert created_user.email == user_data.email
        assert created_user.password == password_hasher.hash(user_data.password)

    def test_login_success(self, user_service, user_repository, password_hasher):
        # Given
        user = User(
            id=uuid4(),
            username="test_user",
            email="test@example.com",
            password=password_hasher.hash("password123")
        )
        user_repository.read_by_username.return_value = user
        
        login_data = FakeLoginUserRequest(
            username="test_user",
            password="password123"
        )
        
        # When/Then
        user_service.login(login_data, password_hasher)  # 예외가 발생하지 않아야 함

    def test_login_invalid_password(self, user_service, user_repository, password_hasher):
        # Given
        user = User(
            id=uuid4(),
            username="test_user",
            email="test@example.com",
            password=password_hasher.hash("correct_password")
        )
        user_repository.read_by_username.return_value = user
        
        login_data = FakeLoginUserRequest(
            username="test_user",
            password="wrong_password"
        )
        
        # When/Then
        with pytest.raises(ValueError, match="Invalid password"):
            user_service.login(login_data, password_hasher)

    def test_login_nonexistent_user(self, user_service, user_repository, password_hasher):
        # Given
        user_repository.read_by_username.side_effect = ValueError("User not found")
        
        login_data = FakeLoginUserRequest(
            username="nonexistent",
            password="password123"
        )
        
        # When/Then
        with pytest.raises(ValueError, match="User not found"):
            user_service.login(login_data, password_hasher) 