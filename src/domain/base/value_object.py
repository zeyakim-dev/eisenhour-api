from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValueObject(ABC):
    value: Any

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, ValueObject):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
