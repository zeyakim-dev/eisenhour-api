from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest

from domain.auth.auth_info.exceptions import (
    PasswordChangeNotAllowedError,
    UserIdMismatchError,
)
from domain.auth.auth_info.local_auth_info import LocalAuthInfo
from domain.auth.auth_info.value_objects import AuthType, AuthTypeEnum, HashedPassword
from shared_kernel.time.time_provider import TimeProvider


@dataclass(frozen=True, kw_only=True)
class StubUser:
    id: UUID = field(default_factory=uuid4)
    auth_type: AuthType = field(default_factory=lambda: AuthType(AuthTypeEnum.LOCAL))


@pytest.fixture
def local_user():
    return StubUser()


@pytest.fixture
def google_user():
    return StubUser(auth_type=AuthType(AuthTypeEnum.GOOGLE))


class ExpiredTimeProvider:
    def now(self) -> datetime:
        return datetime.now() - timedelta(days=10)


@pytest.fixture
def expired_time_provider():
    return ExpiredTimeProvider()


@pytest.fixture
def local_user_auth_info(time_provider: TimeProvider, local_user: StubUser):
    return LocalAuthInfo.create(
        time_provider, user_id=local_user.id, hashed_password=HashedPassword("password")
    )


@pytest.fixture
def expired_local_user_auth_info(
    expired_time_provider: ExpiredTimeProvider, local_user: StubUser
):
    return LocalAuthInfo.create(
        expired_time_provider,
        user_id=local_user.id,
        hashed_password=HashedPassword("password"),
    )


@pytest.mark.unit
class TestLocalAuthInfo:
    """LocalAuthInfo 도메인 객체의 테스트."""

    def test_init_success_with_local_auth_type(self, time_provider: TimeProvider):
        local_auth_info = LocalAuthInfo.create(
            time_provider, user_id=uuid4(), hashed_password=HashedPassword("password")
        )
        assert local_auth_info.auth_type == AuthType(AuthTypeEnum.LOCAL)

    def test_init_raises_value_error_with_not_local_auth_type(
        self, time_provider: TimeProvider
    ):
        with pytest.raises(ValueError):
            LocalAuthInfo.create(
                time_provider,
                user_id=uuid4(),
                hashed_password=HashedPassword("password"),
                auth_type=AuthType(AuthTypeEnum.GOOGLE),
            )

    def test_is_password_expired_returns_true_if_expired(
        self, expired_local_user_auth_info: LocalAuthInfo
    ):
        assert expired_local_user_auth_info.is_password_expired()

    def test_is_password_expired_returns_false_if_not_expired(
        self, local_user_auth_info: LocalAuthInfo
    ):
        assert not local_user_auth_info.is_password_expired()

    def test_change_password_successfully_updates_password_and_expiration(
        self,
        time_provider: TimeProvider,
        local_user: StubUser,
        local_user_auth_info: LocalAuthInfo,
    ):
        new_password = HashedPassword("new_password")
        updated_local_user_auth_info = local_user_auth_info.change_password(
            time_provider, user=local_user, new_password=new_password
        )
        assert updated_local_user_auth_info.hashed_password == new_password
        assert (
            updated_local_user_auth_info.password_expired_at
            == updated_local_user_auth_info.updated_at + timedelta(days=90)
        )

    def test_change_password_raises_user_id_mismatch_error(
        self, time_provider: TimeProvider, local_user_auth_info: LocalAuthInfo
    ):
        with pytest.raises(UserIdMismatchError):
            local_user_auth_info.change_password(
                time_provider,
                user=StubUser(),
                new_password=HashedPassword("new_password"),
            )

    def test_change_password_raises_password_change_not_allowed_error(
        self,
        time_provider: TimeProvider,
        local_user: StubUser,
        local_user_auth_info: LocalAuthInfo,
    ):
        wrong_auth_type_user = StubUser(
            id=local_user.id, auth_type=AuthType(AuthTypeEnum.GOOGLE)
        )
        with pytest.raises(PasswordChangeNotAllowedError):
            local_user_auth_info.change_password(
                time_provider,
                user=wrong_auth_type_user,
                new_password=HashedPassword("new_password"),
            )
