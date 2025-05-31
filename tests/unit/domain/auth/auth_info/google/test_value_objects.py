import pytest

from domain.auth.auth_info.google.exceptions import (
    GoogleSubEmptyError,
    GoogleSubTooLongError,
)
from domain.auth.auth_info.google.value_objects import GoogleSub


@pytest.mark.unit
class TestGoogleSub:
    def test_init_success(self):
        """
        정상적인 sub 값으로 GoogleSub가 생성되는지 검증합니다.

        Given: 정상적인 sub 값이 주어졌을 때
        When: GoogleSub를 생성하면
        Then: 해당 값으로 GoogleSub 인스턴스가 생성되어야 한다.
        """
        sub = GoogleSub("valid-sub-123")
        assert sub.value == "valid-sub-123"

    @pytest.mark.parametrize("invalid_value", ["", "   ", None])
    def test_init_raises_empty_error(self, invalid_value):
        """
        비어있거나 공백인 sub 값에 대한 예외 발생을 검증합니다.

        Given: 비어있거나 공백인 sub 값이 주어졌을 때
        When: GoogleSub를 생성하면
        Then: GoogleSubEmptyError가 발생해야 한다.
        """
        with pytest.raises(GoogleSubEmptyError):
            GoogleSub(invalid_value)

    def test_init_raises_too_long_error(self):
        """
        128자를 초과하는 sub 값에 대한 예외 발생을 검증합니다.

        Given: 128자를 초과하는 sub 값이 주어졌을 때
        When: GoogleSub를 생성하면
        Then: GoogleSubTooLongError가 발생해야 한다.
        """
        long_value = "a" * 129
        with pytest.raises(GoogleSubTooLongError):
            GoogleSub(long_value)
