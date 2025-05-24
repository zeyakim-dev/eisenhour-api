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
    """AuthType 값 객체(Value Object)의 동작을 검증하는 단위 테스트."""

    def test_is_google(self, google_auth_type: AuthType):
        """is_google() 메서드가 Google 타입에서 True를 반환하는지 검증한다.

        Given:
            AuthTypeEnum.GOOGLE로 생성된 AuthType 인스턴스.
        When:
            is_google() 메서드를 호출하면.
        Then:
            True를 반환해야 한다.
        """
        assert google_auth_type.is_google()

    def test_is_not_google(self, local_auth_type: AuthType):
        """is_google() 메서드가 Local 타입에서 False를 반환하는지 검증한다.

        Given:
            AuthTypeEnum.LOCAL로 생성된 AuthType 인스턴스.
        When:
            is_google() 메서드를 호출하면.
        Then:
            False를 반환해야 한다.
        """
        assert not local_auth_type.is_google()

    def test_is_local(self, local_auth_type: AuthType):
        """is_local() 메서드가 Local 타입에서 True를 반환하는지 검증한다.

        Given:
            AuthTypeEnum.LOCAL로 생성된 AuthType 인스턴스.
        When:
            is_local() 메서드를 호출하면.
        Then:
            True를 반환해야 한다.
        """
        assert local_auth_type.is_local()

    def test_is_not_local(self, google_auth_type: AuthType):
        """is_local() 메서드가 Google 타입에서 False를 반환하는지 검증한다.

        Given:
            AuthTypeEnum.GOOGLE로 생성된 AuthType 인스턴스.
        When:
            is_local() 메서드를 호출하면.
        Then:
            False를 반환해야 한다.
        """
        assert not google_auth_type.is_local()
