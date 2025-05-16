from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Self
from uuid import UUID, uuid4

from shared_kernel.time.time_provider import TimeProvider


@dataclass(frozen=True, kw_only=True)
class Command(ABC):
    id: UUID = field(default_factory=uuid4)
    created_at: datetime

    @classmethod
    def create(cls, time_provider: TimeProvider, **kwargs: Any) -> Self:
        kwargs.setdefault("created_at", time_provider.now())
        return cls(**kwargs)
