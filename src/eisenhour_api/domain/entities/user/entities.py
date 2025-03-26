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


class UserFactory:

    @classmethod
    def create(cls, username: str, email: str, hashed_password: str):
        return User(
            username=username,
            email=email,
            password=hashed_password,
        )
