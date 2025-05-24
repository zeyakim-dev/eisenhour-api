from dataclasses import dataclass
from uuid import UUID

from domain.auth.auth_info.value_objects import AuthType, AuthTypeEnum
from domain.base.aggregate import Aggregate


@dataclass(frozen=True, kw_only=True)
class AuthInfo(Aggregate):
    user_id: UUID
    auth_type: AuthType

    def is_google_auth(self) -> bool:
        return self.auth_type.value == AuthTypeEnum.GOOGLE

    def is_local_auth(self) -> bool:
        return self.auth_type.value == AuthTypeEnum.LOCAL
