from datetime import datetime, timedelta, timezone

import pytest

from domain.user.exceptions import (
    PasswordMissingLowercaseError,
    PasswordMissingNumberError,
    PasswordMissingSpecialCharacterError,
    PasswordMissingUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
)
from domain.user.user import User
from domain.user.value_objects import Email, HashedPassword, PlainPassword, UserName
from shared_kernel.hasher.hasher import Hasher
from shared_kernel.time.time_provider import TimeProvider


class FakeHasher(Hasher):
    def hash(self, password: str) -> str:
        return "hashed_" + password

    def verify(self, password: str, hashed_password: str) -> bool:
        return "hashed_" + password == hashed_password


class FakeTimeProvider(TimeProvider):
    def now(self) -> datetime:
        return datetime(2024, 1, 1)


class TestUserEntity:
    @pytest.fixture
    def time_provider(self) -> TimeProvider:
        kst_tz = timezone(timedelta(hours=9))
        return FakeTimeProvider(kst_tz)

    @pytest.fixture
    def user(self, time_provider: TimeProvider) -> User:
        return User.create(
            time_provider=time_provider,
            name=UserName("테스트유저"),
            email=Email("test@example.com"),
            hashed_password=HashedPassword("hashed_Correct_pw_123!"),
        )

    def test_authenticate_success(self, user, time_provider: TimeProvider):
        hasher = FakeHasher()
        result = user.authenticate(PlainPassword("Correct_pw_123!"), hasher)
        assert result is True

    def test_authenticate_failure(self, user, time_provider: TimeProvider):
        hasher = FakeHasher()
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
        self, user, time_provider: TimeProvider, invalid_password, expected_exception
    ):
        hasher = FakeHasher()
        with pytest.raises(expected_exception):
            user.authenticate(PlainPassword(invalid_password), hasher)

    def test_change_password_success(self, user, time_provider: TimeProvider):
        hasher = FakeHasher()
        new_user = user.change_password(
            time_provider=time_provider,
            plain_password=PlainPassword("NewPw123!"),
            hasher=hasher,
        )

        assert new_user.hashed_password.value == "hashed_NewPw123!"
        assert new_user is not user  # 불변 객체이므로 새 인스턴스 반환

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
        self, user, time_provider: TimeProvider, invalid_password, expected_exception
    ):
        hasher = FakeHasher()
        with pytest.raises(expected_exception):
            user.change_password(
                time_provider=time_provider,
                plain_password=PlainPassword(invalid_password),
                hasher=hasher,
            )
