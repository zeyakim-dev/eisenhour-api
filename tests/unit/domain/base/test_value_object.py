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
        a = IntVO(1)
        b = IntVO(1)
        assert a == b
        assert not (a != b)

    def test_not_equal_different_value(self):
        a = IntVO(1)
        b = IntVO(2)
        assert a != b
        assert not (a == b)

    def test_not_equal_different_vo_type(self):
        a = IntVO(1)
        b = StrVO("1")
        assert a != b
        assert not (a == b)

    def test_not_equal_plain_type(self):
        a = IntVO(1)
        assert a != 1
        assert not (a == 1)

    def test_hash_consistency(self):
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
        @dataclass(frozen=True)
        class GenericVO(ValueObject):
            value: Any

        a = GenericVO(v1)
        b = GenericVO(v2)
        assert (a == b) is expected
