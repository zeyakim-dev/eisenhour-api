from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from application.messaging.command.base.command import Command

C = TypeVar("C", bound=Command)


@dataclass(frozen=True)
class CommandResult(ABC):
    pass


R = TypeVar("R", bound=CommandResult)


class CommandHandler(ABC, Generic[C, R]):
    @abstractmethod
    async def execute(self, command: C) -> R:
        raise NotImplementedError
