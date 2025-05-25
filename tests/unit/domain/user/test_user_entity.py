import pytest

from domain.auth.auth_info.value_objects import HashedPassword
from domain.user.exceptions import (
    PasswordMissingLowercaseError,
    PasswordMissingNumberError,
    PasswordMissingSpecialCharacterError,
    PasswordMissingUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
)
from domain.user.user import User
from domain.user.value_objects import Email, PlainPassword, Username
from tests.unit.conftest import FakeHasher, FakeTimeProvider


@pytest.fixture
def user(time_provider: FakeTimeProvider) -> User:
    return User.create(
        time_provider=time_provider,
        username=Username("테스트유저"),
        email=Email("test@example.com"),
        hashed_password=HashedPassword("hashed_Correct_pw_123!"),
    )


class TestUserEntity:
    def test_authenticate_success(self, user, hasher: FakeHasher):
        result = user.authenticate(PlainPassword("Correct_pw_123!"), hasher)
        assert result is True

    def test_authenticate_failure(self, user, hasher: FakeHasher):
        wrong_password = "Wrong_pw_123!"
        result = user.authenticate(PlainPassword(wrong_password), hasher)
        assert result is False

    @pytest.mark.parametrize(
        "invalid_password,expected_exception",
        [
            ("A1a!", PasswordTooShortError),
            ("A" * 101 + "1a!", PasswordTooLongError),
            ("abcd1234!", PasswordMissingUppercaseError),
            ("ABCD1234!", PasswordMissingLowercaseError),
            ("Abcdefgh!", PasswordMissingNumberError),
            ("Abcd1234", PasswordMissingSpecialCharacterError),
        ],
    )
    def test_authenticate_invalid_password(
        self, user, invalid_password, expected_exception
    ):
        hasher = FakeHasher()
        with pytest.raises(expected_exception):
            user.authenticate(PlainPassword(invalid_password), hasher)

    def test_change_password_success(
        self, user, time_provider: FakeTimeProvider, hasher: FakeHasher
    ):
        new_user = user.change_password(
            time_provider=time_provider,
            plain_password=PlainPassword("NewPw123!"),
            hasher=hasher,
        )

        assert new_user.hashed_password.value == "hashed_NewPw123!"
        assert new_user is not user

    @pytest.mark.parametrize(
        "invalid_password,expected_exception",
        [
            ("A1a!", PasswordTooShortError),
            ("A" * 101 + "1a!", PasswordTooLongError),
            ("abcd1234!", PasswordMissingUppercaseError),
            ("ABCD1234!", PasswordMissingLowercaseError),
            ("Abcdefgh!", PasswordMissingNumberError),
            ("Abcd1234", PasswordMissingSpecialCharacterError),
        ],
    )
    def test_change_password_invalid(
        self,
        user,
        time_provider: FakeTimeProvider,
        invalid_password,
        expected_exception,
    ):
        hasher = FakeHasher()
        with pytest.raises(expected_exception):
            user.change_password(
                time_provider=time_provider,
                plain_password=PlainPassword(invalid_password),
                hasher=hasher,
            )
