from dataclasses import dataclass

from domain.base.value_object import ValueObject


@dataclass(frozen=True)
class UserName(ValueObject):
    value: str


@dataclass(frozen=True)
class Email(ValueObject):
    value: str


@dataclass(frozen=True)
class Password(ValueObject):
    value: str
