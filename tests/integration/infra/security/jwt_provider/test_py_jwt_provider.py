from datetime import datetime, timedelta, timezone

import jwt
import pytest

from infra.security.jwt_provider.py_jwt_provider import PyJWTProvider
from shared_kernel.time.time_provider import TimeProvider


class FixedTimeProvider(TimeProvider):
    def __init__(self, now: datetime) -> None:
        self.kst = timezone(timedelta(hours=9))
        super().__init__(self.kst)
        self.fixed_now = now.replace(tzinfo=self.kst)

    def now(self) -> datetime:
        return self.fixed_now


@pytest.fixture
def time_provider():
    return TimeProvider(timezone(timedelta(hours=9)))


@pytest.fixture
def fixed_time_provider():
    return FixedTimeProvider(datetime(2000, 1, 1, 12, 0, 0))


@pytest.fixture
def jwt_provider(time_provider):
    return PyJWTProvider(time_provider, secret="testsecret", algorithm="HS256")


@pytest.fixture
def expired_jwt_provider(fixed_time_provider):
    return PyJWTProvider(fixed_time_provider, secret="testsecret", algorithm="HS256")


@pytest.mark.integration
class TestPyJWTProvider:
    def test_encode_decode_success(self, jwt_provider):
        """
        JWT 토큰의 encode/decode가 정상적으로 동작하는지 검증합니다.

        Given: user_id, role 등 payload와 만료시간이 주어졌을 때
        When: encode로 토큰을 발급하고 decode로 복호화하면
        Then: 원래 payload와 exp 클레임이 정확히 복원되어야 한다.
        """
        payload = {"user_id": "abc123", "role": "user"}
        token = jwt_provider.encode(payload, expires_in=3600)
        decoded = jwt_provider.decode(token)
        assert decoded["user_id"] == "abc123"
        assert decoded["role"] == "user"
        assert "exp" in decoded

    def test_is_valid_true(self, jwt_provider):
        """
        정상 토큰의 is_valid가 True를 반환하는지 검증합니다.

        Given: 정상적으로 발급된 토큰이 있을 때
        When: is_valid를 호출하면
        Then: True를 반환해야 한다.
        """
        token = jwt_provider.encode({"user_id": "abc"}, expires_in=100)
        assert jwt_provider.is_valid(token) is True

    def test_is_valid_false(self, jwt_provider):
        """
        잘못된 토큰의 is_valid가 False를 반환하는지 검증합니다.

        Given: 임의의 잘못된 문자열이 토큰으로 주어졌을 때
        When: is_valid를 호출하면
        Then: False를 반환해야 한다.
        """
        assert jwt_provider.is_valid("not_a_jwt_token") is False

    def test_expired_token(self, expired_jwt_provider):
        """
        만료된 토큰의 decode가 예외를 발생시키고, is_valid가 False를 반환하는지 검증합니다.

        Given: 이미 만료된(exp=0) 토큰이 있을 때
        When: decode를 호출하면
        Then: ExpiredSignatureError 예외가 발생하고, is_valid는 False를 반환해야 한다.
        """
        provider = expired_jwt_provider
        token = provider.encode({"user_id": "abc"}, expires_in=0)
        with pytest.raises(jwt.ExpiredSignatureError):
            provider.decode(token)
        assert provider.is_valid(token) is False

    def test_token_tampering(self, jwt_provider):
        """
        토큰 페이로드를 임의로 변조했을 때 decode/is_valid가 실패하는지 검증합니다.

        Given: 정상 토큰을 임의로 변조한 경우
        When: decode를 호출하면
        Then: InvalidTokenError 예외가 발생하고, is_valid는 False를 반환해야 한다.
        """
        payload = {"user_id": "abc123"}
        token = jwt_provider.encode(payload, expires_in=3600)
        tampered_token = token[:-1] + ("a" if token[-1] != "a" else "b")
        with pytest.raises(jwt.InvalidTokenError):
            jwt_provider.decode(tampered_token)
        assert jwt_provider.is_valid(tampered_token) is False
