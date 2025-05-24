import pytest

from domain.auth.auth_info.value_objects import AuthType, AuthTypeEnum


@pytest.fixture
def google_auth_type() -> AuthType:
    return AuthType(AuthTypeEnum.GOOGLE)


@pytest.fixture
def local_auth_type() -> AuthType:
    return AuthType(AuthTypeEnum.LOCAL)


@pytest.mark.unit
class TestAuthTypeVO:
    def test_is_google(self, google_auth_type: AuthType):
        assert google_auth_type.is_google()

    def test_is_not_google(self, local_auth_type: AuthType):
        assert not local_auth_type.is_google()

    def test_is_local(self, local_auth_type: AuthType):
        assert local_auth_type.is_local()

    def test_is_not_local(self, google_auth_type: AuthType):
        assert not google_auth_type.is_local()
