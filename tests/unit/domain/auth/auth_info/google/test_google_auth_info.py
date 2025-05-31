"""
GoogleAuthInfo 도메인 객체의 단위 테스트.
"""

from datetime import datetime
from uuid import uuid4

import pytest

from domain.auth.auth_info.base.value_objects import AuthType, AuthTypeEnum
from domain.auth.auth_info.google.google_auth_info import GoogleAuthInfo
from domain.auth.auth_info.google.value_objects import GoogleSub


@pytest.fixture
def google_auth_info():
    """
    기본 GoogleAuthInfo 인스턴스 픽스쳐
    """
    return GoogleAuthInfo.create(
        now=datetime.now(),
        user_id=uuid4(),
        sub=GoogleSub("sub-123"),
        avatar_url="https://example.com/avatar.png",
    )


@pytest.mark.unit
class TestGoogleAuthInfo:
    def test_init_success_with_google_auth_type(self, google_auth_info):
        """
        GoogleAuthInfo가 정상적으로 초기화되는지 검증합니다.

        Given: GoogleAuthInfo를 생성할 때
        When: GOOGLE 타입, sub, avatar_url을 지정하면
        Then: 올바르게 초기화되어야 한다.
        """
        assert google_auth_info.auth_type == AuthType(AuthTypeEnum.GOOGLE)
        assert google_auth_info.sub.value == "sub-123"
        assert google_auth_info.avatar_url == "https://example.com/avatar.png"

    def test_validate_auth_type_returns_true(self, google_auth_info):
        """
        validate_auth_type() 동작을 검증합니다.

        Given: GoogleAuthInfo 인스턴스가 있을 때
        When: validate_auth_type()을 호출하면
        Then: GOOGLE 타입이면 True를 반환해야 한다.
        """
        assert google_auth_info.validate_auth_type() is True

    def test_update_avatar_url_success(self, google_auth_info):
        """
        update_avatar_url()이 정상적으로 avatar_url을 변경하는지 검증합니다.

        Given: 기존 GoogleAuthInfo 인스턴스가 있을 때
        When: update_avatar_url()로 새로운 URL을 지정하면
        Then: avatar_url이 변경된 새 인스턴스가 반환되어야 한다.
        """
        new_url = "https://example.com/new_avatar.png"
        now = datetime.now()
        updated = google_auth_info.update_avatar_url(now, new_url)
        assert updated.avatar_url == new_url
        assert updated is not google_auth_info
