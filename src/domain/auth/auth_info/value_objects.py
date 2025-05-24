from dataclasses import dataclass, field
from enum import Enum

from domain.base.value_object import ValueObject


class AuthTypeEnum(Enum):
    LOCAL = "LOCAL"
    GOOGLE = "GOOGLE"


@dataclass(frozen=True, kw_only=True)
class AuthType(ValueObject[AuthTypeEnum]):
    value: AuthTypeEnum = field(default=AuthTypeEnum.LOCAL)

    def is_google(self) -> bool:
        return self.value == AuthTypeEnum.GOOGLE

    def is_local(self) -> bool:
        return self.value == AuthTypeEnum.LOCAL
