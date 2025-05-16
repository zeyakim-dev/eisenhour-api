from application.messaging.command.base.command_handler import CommandHandler
from application.messaging.command.user.user_register_command import (
    UserRegisterCommand,
    UserRegisterCommandResult,
)
from domain.user.repository.user_repository import UserRepository
from domain.user.user import User
from domain.user.value_objects import Email, HashedPassword, PlainPassword, Username
from shared_kernel.hasher.hasher import Hasher
from shared_kernel.time.time_provider import TimeProvider


class UserRegisterCommandHandler(
    CommandHandler[UserRegisterCommand, UserRegisterCommandResult]
):
    def __init__(
        self, repository: UserRepository, time_provider: TimeProvider, hasher: Hasher
    ) -> None:
        self.repository = repository
        self.time_provider = time_provider
        self.hasher = hasher

    def execute(self, command: UserRegisterCommand) -> UserRegisterCommandResult:
        username = Username(command.username)
        email = Email(command.email)
        plain_password = PlainPassword(command.plain_password)

        hashed_password_value = self.hasher.hash(plain_password.value)
        hashed_password = HashedPassword(hashed_password_value)

        user = User.create(
            time_provider=self.time_provider,
            username=username,
            email=email,
            hashed_password=hashed_password,
        )

        self.repository.save(user)

        return UserRegisterCommandResult(
            id=str(user.id), username=user.username.value, email=user.email.value
        )
