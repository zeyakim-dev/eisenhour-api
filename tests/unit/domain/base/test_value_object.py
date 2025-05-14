from dataclasses import dataclass
from typing import Any

import pytest

from domain.base.value_object import ValueObject


@dataclass(frozen=True)
class IntVO(ValueObject):
    value: int


@dataclass(frozen=True)
class StrVO(ValueObject):
    value: str


class TestValueObject:
    def test_equal_same_value(self):
        """동일한 값을 가진 같은 타입의 ValueObject는 동등해야 한다."""
        a = IntVO(1)
        b = IntVO(1)
        assert a == b
        assert not (a != b)

    def test_not_equal_different_value(self):
        """값이 다른 같은 타입의 ValueObject는 동등하지 않아야 한다."""
        a = IntVO(1)
        b = IntVO(2)
        assert a != b
        assert not (a == b)

    def test_not_equal_different_vo_type(self):
        """타입이 다른 ValueObject는 값이 같더라도 동등하지 않아야 한다."""
        a = IntVO(1)
        b = StrVO("1")
        assert a != b
        assert not (a == b)

    def test_not_equal_plain_type(self):
        """ValueObject는 원시 타입과 비교 시 항상 동등하지 않아야 한다."""
        a = IntVO(1)
        assert a != 1
        assert not (a == 1)

    def test_hash_consistency(self):
        """동일한 값을 가진 ValueObject의 해시값은 동일해야 한다."""
        a = IntVO(42)
        b = IntVO(42)
        assert hash(a) == hash(b)
        s = {a, b}
        assert len(s) == 1

    @pytest.mark.parametrize(
        "v1,v2,expected",
        [
            (None, None, True),
            (None, 0, False),
            ("a", "a", True),
            ("a", "b", False),
        ],
    )
    def test_edge_cases_generic_vo(self, v1: Any, v2: Any, expected: bool):
        """다양한 타입의 값 비교에 대한 제너릭 ValueObject 동작을 검증한다.

        Args:
            v1 (Any): 첫 번째 값.
            v2 (Any): 두 번째 값.
            expected (bool): 두 값이 동등하다고 기대되는지 여부.
        """

        @dataclass(frozen=True)
        class GenericVO(ValueObject):
            value: Any

        a = GenericVO(v1)
        b = GenericVO(v2)
        assert (a == b) is expected
