from dataclasses import dataclass

from domain.base.aggregate import Aggregate
from domain.user.value_objects import Email, HashedPassword, UserName


@dataclass(frozen=True, kw_only=True)
class User(Aggregate):
    name: UserName
    email: Email
    hashed_password: HashedPassword
