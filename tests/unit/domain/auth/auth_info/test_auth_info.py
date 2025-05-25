from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

import pytest

from domain.auth.auth_info.auth_info import AuthInfo
from domain.auth.auth_info.exceptions import InvalidAuthTypeError
from domain.auth.auth_info.value_objects import AuthType, AuthTypeEnum


@dataclass(frozen=True, kw_only=True)
class GoogleOAuthInfo(AuthInfo):
    auth_type: AuthType = field(default_factory=lambda: AuthType(AuthTypeEnum.GOOGLE))

    def validate_auth_type(self) -> bool:
        return self.auth_type.is_google()


@dataclass(frozen=True, kw_only=True)
class LocalAuthInfo(AuthInfo):
    auth_type: AuthType = field(default_factory=lambda: AuthType(AuthTypeEnum.LOCAL))

    def validate_auth_type(self) -> bool:
        return self.auth_type.is_local()


@pytest.fixture
def google_oauth_info() -> GoogleOAuthInfo:
    return GoogleOAuthInfo.create(now=datetime.now(), user_id=uuid4())


@pytest.fixture
def local_auth_info() -> LocalAuthInfo:
    return LocalAuthInfo.create(now=datetime.now(), user_id=uuid4())


@pytest.mark.unit
class TestAuthInfo:
    """AuthInfo 및 하위 클래스(GoogleOAuthInfo, LocalAuthInfo)의 단위 테스트."""

    def test_is_google_auth(self, google_oauth_info: GoogleOAuthInfo) -> None:
        """GoogleOAuthInfo 인스턴스의 is_google_auth()와 is_local_auth() 동작을 검증한다.

        Given:
            GoogleOAuthInfo 인스턴스가 준비됨.
        When:
            is_google_auth()와 is_local_auth() 메서드를 호출하면.
        Then:
            is_google_auth()는 True, is_local_auth()는 False를 반환해야 한다.
        """
        assert google_oauth_info.is_google_auth()
        assert not google_oauth_info.is_local_auth()

    def test_is_local_auth(self, local_auth_info: LocalAuthInfo) -> None:
        """LocalAuthInfo 인스턴스의 is_local_auth()와 is_google_auth() 동작을 검증한다.

        Given:
            LocalAuthInfo 인스턴스가 준비됨.
        When:
            is_local_auth()와 is_google_auth() 메서드를 호출하면.
        Then:
            is_local_auth()는 True, is_google_auth()는 False를 반환해야 한다.
        """
        assert local_auth_info.is_local_auth()
        assert not local_auth_info.is_google_auth()

    def test_invalid_auth_type(self) -> None:
        """잘못된 auth_type 주입 시 InvalidAuthTypeError 예외가 발생하는지 검증한다.

        Given:
            GoogleOAuthInfo 또는 LocalAuthInfo에 잘못된 AuthType을 명시적으로 주입함.
        When:
            .create() 메서드로 인스턴스를 생성하려고 시도하면.
        Then:
            InvalidAuthTypeError 예외가 발생해야 한다.
        """
        with pytest.raises(InvalidAuthTypeError):
            GoogleOAuthInfo.create(
                now=datetime.now(),
                user_id=uuid4(),
                auth_type=AuthType(AuthTypeEnum.LOCAL),
            )

        with pytest.raises(InvalidAuthTypeError):
            LocalAuthInfo.create(
                now=datetime.now(),
                user_id=uuid4(),
                auth_type=AuthType(AuthTypeEnum.GOOGLE),
            )
