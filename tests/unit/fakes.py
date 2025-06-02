from abc import ABC
from dataclasses import dataclass, field, replace
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class FakeEntity(ABC):
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, now: datetime, **kwargs):
        kwargs.update({"created_at": now, "updated_at": now})
        return cls(**kwargs)

    def update(self, now: datetime, **kwargs):
        now = now or datetime.now()
        kwargs.update({"updated_at": now})
        return replace(self, **kwargs)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


@dataclass(frozen=True, kw_only=True)
class FakeUser(FakeEntity):
    username: str
    email: str
