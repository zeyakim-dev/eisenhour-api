from abc import abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.auth.auth_info.exceptions import InvalidAuthTypeError
from domain.auth.auth_info.value_objects import AuthType
from domain.base.aggregate import Aggregate


@dataclass(frozen=True, kw_only=True)
class AuthInfo(Aggregate):
    user_id: UUID
    auth_type: AuthType

    def __post_init__(self) -> None:
        if not self.validate_auth_type():
            raise InvalidAuthTypeError(self.auth_type)

    @abstractmethod
    def validate_auth_type(self) -> bool:
        raise NotImplementedError

    def is_google_auth(self) -> bool:
        return self.auth_type.is_google()

    def is_local_auth(self) -> bool:
        return self.auth_type.is_local()
