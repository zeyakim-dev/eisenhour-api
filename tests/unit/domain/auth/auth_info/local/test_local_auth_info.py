from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest

from domain.auth.auth_info.base.exceptions import InvalidAuthTypeError
from domain.auth.auth_info.base.value_objects import AuthType, AuthTypeEnum
from domain.auth.auth_info.local.exceptions import (
    PasswordChangeNotAllowedError,
    UserIdMismatchError,
)
from domain.auth.auth_info.local.local_auth_info import LocalAuthInfo
from domain.auth.auth_info.local.value_objects import HashedPassword
from shared_kernel.time.time_provider import TimeProvider


@dataclass(frozen=True, kw_only=True)
class StubUser:
    id: UUID = field(default_factory=uuid4)
    auth_type: AuthType = field(default_factory=lambda: AuthType(AuthTypeEnum.LOCAL))


@pytest.fixture
def local_user():
    return StubUser()


@pytest.fixture
def local_user_auth_info(local_user: StubUser):
    return LocalAuthInfo.create(
        now=datetime.now(),
        user_id=local_user.id,
        hashed_password=HashedPassword("password"),
    )


@pytest.fixture
def expired_local_user_auth_info(local_user: StubUser):
    return LocalAuthInfo.create(
        now=datetime.now() - timedelta(days=100),
        user_id=local_user.id,
        hashed_password=HashedPassword("password"),
    )


@pytest.mark.unit
class TestLocalAuthInfo:
    """LocalAuthInfo 도메인 객체의 테스트."""

    def test_init_success_with_local_auth_type(self):
        """LOCAL 타입으로 생성 시 정상적으로 초기화되는지 검증한다.

        Given:
            AuthTypeEnum.LOCAL로 생성된 LocalAuthInfo 인스턴스.
        When:
            create() 메서드를 호출하면.
        Then:
            auth_type 필드가 LOCAL로 설정되어야 한다.
        """
        local_auth_info = LocalAuthInfo.create(
            now=datetime.now(),
            user_id=uuid4(),
            hashed_password=HashedPassword("password"),
        )
        assert local_auth_info.auth_type == AuthType(AuthTypeEnum.LOCAL)

    def test_init_raises_value_error_with_not_local_auth_type(
        self, time_provider: TimeProvider
    ):
        """LOCAL 이외의 auth_type으로 생성 시 InvalidAuthTypeError가 발생하는지 검증한다.

        Given:
            AuthTypeEnum.GOOGLE로 생성 요청.
        When:
            LocalAuthInfo.create()를 호출하면.
        Then:
            InvalidAuthTypeError 예외가 발생해야 한다.
        """
        with pytest.raises(InvalidAuthTypeError):
            LocalAuthInfo.create(
                now=datetime.now(),
                user_id=uuid4(),
                hashed_password=HashedPassword("password"),
                auth_type=AuthType(AuthTypeEnum.GOOGLE),
            )

    def test_is_password_expired_returns_true_if_expired(
        self, expired_local_user_auth_info: LocalAuthInfo
    ):
        """만료일이 현재보다 이전이면 is_password_expired()가 True를 반환하는지 검증한다.

        Given:
            password_expired_at이 100일 전으로 설정된 LocalAuthInfo.
        When:
            is_password_expired()를 호출하면.
        Then:
            True를 반환해야 한다.
        """
        assert expired_local_user_auth_info.is_password_expired(datetime.now())

    def test_is_password_expired_returns_false_if_not_expired(
        self, local_user_auth_info: LocalAuthInfo
    ):
        """만료일이 현재보다 이후이면 is_password_expired()가 False를 반환하는지 검증한다.

        Given:
            password_expired_at이 미래로 설정된 LocalAuthInfo.
        When:
            is_password_expired()를 호출하면.
        Then:
            False를 반환해야 한다.
        """
        assert not local_user_auth_info.is_password_expired(datetime.now())

    def test_change_password_successfully_updates_password_and_expiration(
        self,
        local_user: StubUser,
        local_user_auth_info: LocalAuthInfo,
    ):
        """비밀번호 변경 시 비밀번호와 만료일이 갱신되는지 검증한다.

        Given:
            현재 비밀번호가 설정된 LocalAuthInfo와 Local 사용자.
        When:
            change_password()를 호출해 새 비밀번호를 설정하면.
        Then:
            hashed_password가 갱신되고, password_expired_at이 updated_at + 90일로 설정되어야 한다.
        """
        new_password = HashedPassword("new_password")
        updated_local_user_auth_info = local_user_auth_info.change_password(
            now=datetime.now(), user=local_user, new_password=new_password
        )
        assert updated_local_user_auth_info.hashed_password == new_password
        assert (
            updated_local_user_auth_info.password_expired_at
            == updated_local_user_auth_info.updated_at + timedelta(days=90)
        )

    def test_change_password_raises_user_id_mismatch_error(
        self, time_provider: TimeProvider, local_user_auth_info: LocalAuthInfo
    ):
        """user_id 불일치 시 UserIdMismatchError가 발생하는지 검증한다.

        Given:
            다른 user_id를 가진 사용자.
        When:
            change_password()를 호출하면.
        Then:
            UserIdMismatchError 예외가 발생해야 한다.
        """
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
        """auth_type이 LOCAL이 아닐 때 PasswordChangeNotAllowedError가 발생하는지 검증한다.

        Given:
            auth_type이 GOOGLE인 사용자.
        When:
            change_password()를 호출하면.
        Then:
            PasswordChangeNotAllowedError 예외가 발생해야 한다.
        """
        wrong_auth_type_user = StubUser(
            id=local_user.id, auth_type=AuthType(AuthTypeEnum.GOOGLE)
        )
        with pytest.raises(PasswordChangeNotAllowedError):
            local_user_auth_info.change_password(
                time_provider,
                user=wrong_auth_type_user,
                new_password=HashedPassword("new_password"),
            )
