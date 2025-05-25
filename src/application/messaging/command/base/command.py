from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Self
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class Command(ABC):
    id: UUID = field(default_factory=uuid4)
    created_at: datetime

    @classmethod
    def create(cls, now: datetime, **kwargs: Any) -> Self:
        kwargs.setdefault("created_at", now)
        return cls(**kwargs)
