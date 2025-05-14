from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Any, Self
from uuid import UUID, uuid4

from domain.base.exceptions import TimestampRequiredError
from shared_kernel.time.time_provider import TimeProvider


@dataclass(frozen=True, kw_only=True)
class Entity:
    id: UUID = field(default_factory=uuid4)
    created_at: datetime
    updated_at: datetime

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __post_init__(self) -> None:
        if self.created_at is None or self.updated_at is None:
            raise TimestampRequiredError()

    @classmethod
    def create(cls, time_provider: TimeProvider, **kwargs: Any) -> Self:
        now = time_provider.now()
        kwargs.setdefault("created_at", now)
        kwargs.setdefault("updated_at", now)
        return cls(**kwargs)

    def update(self, time_provider: TimeProvider, **kwargs: Any) -> Self:
        now = time_provider.now()
        kwargs.setdefault("updated_at", now)
        return replace(self, **kwargs)
