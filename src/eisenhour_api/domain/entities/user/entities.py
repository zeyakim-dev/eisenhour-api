from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
import uuid


@dataclass(frozen=True, kw_only=True)
class User:
    id: UUID = field(default_factory=uuid.uuid4)
    username: str
    email: str
    password: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
