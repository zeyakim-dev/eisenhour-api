from dataclasses import dataclass, field
from uuid import uuid4

import pytest

from domain.auth.auth_info.auth_info import AuthInfo
from domain.auth.auth_info.exceptions import InvalidAuthTypeError
from domain.auth.auth_info.value_objects import AuthType, AuthTypeEnum
from shared_kernel.time.time_provider import TimeProvider


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
def google_oauth_info(time_provider: TimeProvider) -> GoogleOAuthInfo:
    return GoogleOAuthInfo.create(time_provider=time_provider, user_id=uuid4())


@pytest.fixture
def local_auth_info(time_provider: TimeProvider) -> LocalAuthInfo:
    return LocalAuthInfo.create(time_provider=time_provider, user_id=uuid4())


@pytest.mark.unit
class TestAuthInfo:
    def test_is_google_auth(self, google_oauth_info: GoogleOAuthInfo) -> None:
        assert google_oauth_info.is_google_auth()
        assert not google_oauth_info.is_local_auth()

    def test_is_local_auth(self, local_auth_info: LocalAuthInfo) -> None:
        assert local_auth_info.is_local_auth()
        assert not local_auth_info.is_google_auth()

    def test_invalid_auth_type(self, time_provider: TimeProvider) -> None:
        with pytest.raises(InvalidAuthTypeError):
            GoogleOAuthInfo.create(
                time_provider=time_provider,
                user_id=uuid4(),
                auth_type=AuthType(AuthTypeEnum.LOCAL),
            )

        with pytest.raises(InvalidAuthTypeError):
            LocalAuthInfo.create(
                time_provider=time_provider,
                user_id=uuid4(),
                auth_type=AuthType(AuthTypeEnum.GOOGLE),
            )
