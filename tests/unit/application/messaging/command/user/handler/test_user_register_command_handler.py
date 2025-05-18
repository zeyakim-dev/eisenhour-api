import pytest

from application.messaging.command.user.handler.user_register_command_handler import (
    UserRegisterCommandHandler,
)
from application.messaging.command.user.user_register_command import UserRegisterCommand
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)


@pytest.fixture
def user_register_command_handler(fake_user_inmemory_repository, time_provider, hasher):
    return UserRegisterCommandHandler(
        repository=fake_user_inmemory_repository,
        time_provider=time_provider,
        hasher=hasher,
    )


@pytest.mark.asyncio
class TestUserRegisterCommand:
    async def test_successful_registration(
        self, user_register_command_handler, time_provider
    ):
        command = UserRegisterCommand.create(
            time_provider=time_provider,
            username="newuser",
            email="newuser@example.com",
            plain_password="Secret_123!",
        )

        result = await user_register_command_handler.execute(command)
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"

    async def test_duplicate_username_raises_error(
        self, user_register_command_handler, time_provider, valid_user1
    ):
        command = UserRegisterCommand.create(
            time_provider=time_provider,
            username=valid_user1.username,
            email="unique@example.com",
            plain_password="Secret_123!",
        )

        with pytest.raises(UsernameAlreadyExistsError):
            await user_register_command_handler.execute(command)

    async def test_duplicate_email_raises_error(
        self, user_register_command_handler, time_provider, valid_user2
    ):
        command = UserRegisterCommand.create(
            time_provider=time_provider,
            username="uniqueuser",
            email=valid_user2.email,
            plain_password="Secret_123!",
        )

        with pytest.raises(EmailAlreadyExistsError):
            await user_register_command_handler.execute(command)
