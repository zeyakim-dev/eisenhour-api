from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

V = TypeVar("V", bound=object)


@dataclass(frozen=True)
class ValueObject(ABC, Generic[V]):
    """값 객체(Value Object)의 추상 기반 클래스입니다.

    값 객체는 동일성(identity)이 아닌 값(value)으로 객체를 비교합니다.
    이 클래스는 불변성을 갖고 있으며, 내부 값에 기반한 동등성 비교와 해시를 제공합니다.

    Attributes:
        value (V): 비교 및 해시에 사용되는 내부 값.
    """

    value: V

    def __eq__(self, other: object) -> bool:
        """동등성 비교 연산자.

        Args:
            other (object): 비교 대상 객체.

        Returns:
            bool: 두 값 객체가 동등하면 True, 그렇지 않으면 False.
                 다른 타입일 경우 False를 반환.
        """
        if not isinstance(other, ValueObject):
            return False
        other = cast(ValueObject[V], other)

        return self.value == other.value

    def __hash__(self) -> int:
        """해시 값을 반환합니다.

        Returns:
            int: 내부 값에 기반한 해시 값.
        """
        return hash(self.value)
