from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

V = TypeVar("V", bound=object)


@dataclass(frozen=True)
class ValueObject(ABC, Generic[V]):
    """값 객체(Value Object)의 추상 기반 클래스입니다.

    동일성이 아닌 내부 값으로 객체를 비교하는 불변 객체입니다.
    내부 값(value)에 기반한 동등성 비교와 해시 구현을 제공합니다.

    Attributes:
        value (V): 값 객체의 비교 및 해시 기준이 되는 내부 값.
    """

    value: V

    def __eq__(self, other: object) -> bool:
        """값 객체 간의 동등성을 비교합니다.

        Args:
            other (object): 비교 대상 객체.

        Returns:
            bool: 두 객체가 동일한 ValueObject 타입이며, 내부 값이 같으면 True.
                  타입이 다르면 False.
        """
        if not isinstance(other, ValueObject):
            return False
        other = cast(ValueObject[V], other)
        return self.value == other.value

    def __hash__(self) -> int:
        """내부 값에 기반한 해시 값을 반환합니다.

        Returns:
            int: 내부 값을 기준으로 생성된 해시 값.
        """
        return hash(self.value)
