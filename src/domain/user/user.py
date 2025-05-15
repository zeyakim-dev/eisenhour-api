from dataclasses import dataclass

from domain.base.aggregate import Aggregate


@dataclass(frozen=True, kw_only=True)
class User(Aggregate):
    name: str
    email: str
    password: str
