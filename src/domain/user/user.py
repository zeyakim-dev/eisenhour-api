from dataclasses import dataclass

from domain.base.aggregate import Aggregate
from domain.user.value_objects import Email, HashedPassword, PlainPassword, UserName
from shared_kernel.hasher.hasher import Hasher
from shared_kernel.time_provider.time_provider import TimeProvider


@dataclass(frozen=True, kw_only=True)
class User(Aggregate):
    name: UserName
    email: Email
    hashed_password: HashedPassword

    def authenticate(self, plain_password: PlainPassword, hasher: Hasher) -> bool:
        return hasher.verify(plain_password.value, self.hashed_password.value)

    def change_password(
        self, time_provider: TimeProvider, plain_password: PlainPassword, hasher: Hasher
    ) -> None:
        new_hashed_password: HashedPassword = HashedPassword(
            hasher.hash(plain_password.value)
        )
        self.update(time_provider=time_provider, hashed_password=new_hashed_password)
