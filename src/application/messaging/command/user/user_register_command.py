from dataclasses import dataclass

from application.messaging.command.base.command import Command
from application.messaging.command.base.command_handler import CommandResult


@dataclass(frozen=True, kw_only=True)
class UserRegisterCommand(Command):
    username: str
    email: str
    plain_password: str


@dataclass(frozen=True, kw_only=True)
class UserRegisterCommandResult(CommandResult):
    id: str
    username: str
    email: str
