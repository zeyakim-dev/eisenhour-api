import pytest

from application.messaging.command.user.handler.user_register_command_handler import (
    UserRegisterCommandHandler,
)
from application.messaging.command.user.user_register_command import UserRegisterCommand
from domain.auth.auth_info.base.value_objects import AuthTypeEnum
from domain.auth.auth_info.local.local_auth_info import LocalAuthInfo
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from domain.user.user import User
from shared_kernel.time.time_provider import TimeProvider


@pytest.fixture
def repositories(
    fake_user_inmemory_repository, fake_local_auth_info_inmemory_repository
):
    return {
        User: fake_user_inmemory_repository,
        LocalAuthInfo: fake_local_auth_info_inmemory_repository,
    }


@pytest.fixture
def user_register_command_handler(repositories, time_provider, hasher):
    return UserRegisterCommandHandler(
        repositories=repositories,
        time_provider=time_provider,
        hasher=hasher,
    )


@pytest.mark.asyncio
class TestUserRegisterCommand:
    async def test_successful_registration(
        self,
        user_register_command_handler: UserRegisterCommandHandler,
        time_provider: TimeProvider,
    ):
        command = UserRegisterCommand.create(
            now=time_provider.now(),
            username="newuser",
            email="newuser@example.com",
            plain_password="Secret_123!",
        )

        result = await user_register_command_handler.execute(command)
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"
        assert result.auth_type == AuthTypeEnum.LOCAL.value

    async def test_duplicate_username_raises_error(
        self, user_register_command_handler, time_provider, valid_user1
    ):
        command = UserRegisterCommand.create(
            now=time_provider.now(),
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
            now=time_provider.now(),
            username="uniqueuser",
            email=valid_user2.email,
            plain_password="Secret_123!",
        )

        with pytest.raises(EmailAlreadyExistsError):
            await user_register_command_handler.execute(command)
