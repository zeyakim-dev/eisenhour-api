from datetime import datetime

import pytest

from application.messaging.command.auth.local.handler.exceptions import (
    WrongPasswordError,
)
from application.messaging.command.auth.local.handler.local_user_authenticate_command_handler import (
    LocalUserAuthenticateCommandHandler,
)
from application.messaging.command.auth.local.local_user_authenticate_command import (
    LocalUserAuthenticateCommand,
)
from domain.auth.auth_info.local.repository.exceptions import LocalAuthInfoNotFoundError
from domain.user.repository.exceptions import UsernameNotFoundError
from tests.unit.conftest import FakeUserEntity


class FakeJWTProvider:
    def encode(self, payload, expires_in, additional_claims=None):
        return f"token_for_{payload.get('username', payload.get('user_id', 'unknown'))}_{payload['type']}"

    def decode(self, token):
        return {"user_id": "some-id", "type": "access"}

    def is_valid(self, token):
        return True


@pytest.fixture
def repositories(
    fake_user_inmemory_repository, fake_local_auth_info_inmemory_repository
):
    return {
        "user": fake_user_inmemory_repository,
        "local_auth_info": fake_local_auth_info_inmemory_repository,
    }


@pytest.fixture
def jwt_provider():
    return FakeJWTProvider()


@pytest.fixture
def authenticate_command_handler(repositories, hasher, jwt_provider):
    return LocalUserAuthenticateCommandHandler(
        repositories=repositories,
        hasher=hasher,
        jwt_provider=jwt_provider,
    )


@pytest.mark.asyncio
class TestLocalUserAuthenticateCommand:
    async def test_successful_authentication(
        self, authenticate_command_handler, valid_user1: FakeUserEntity
    ):
        """GIVEN: 올바른 username, password WHEN: execute 호출 THEN: access/refresh 토큰과 사용자 정보가 반환된다."""
        command = LocalUserAuthenticateCommand.create(
            now=datetime.now(),
            username=valid_user1.username.value,
            plain_password="Test_pw_1!",
        )
        result = await authenticate_command_handler.execute(command)
        assert result.username == valid_user1.username.value
        assert result.email == valid_user1.email.value
        assert result.access_token.startswith(
            f"token_for_{valid_user1.username.value}_access"
        )
        assert result.refresh_token.startswith(
            f"token_for_{valid_user1.username.value}_refresh"
        )

    async def test_wrong_password_raises_error(
        self, authenticate_command_handler, valid_user1
    ):
        """GIVEN: 올바르지 않은 password WHEN: execute 호출 THEN: WrongPasswordError가 발생한다."""
        command = LocalUserAuthenticateCommand.create(
            now=datetime.now(),
            username=valid_user1.username.value,
            plain_password="Wrong_pw_123!",
        )
        with pytest.raises(WrongPasswordError):
            await authenticate_command_handler.execute(command)

    async def test_nonexistent_user_raises_error(self, authenticate_command_handler):
        """GIVEN: 존재하지 않는 username WHEN: execute 호출 THEN: UsernameNotFoundError가 발생한다."""
        command = LocalUserAuthenticateCommand.create(
            now=datetime.now(),
            username="not_exist_user",
            plain_password="Irrelevant_pw_123!",
        )
        with pytest.raises(UsernameNotFoundError):
            await authenticate_command_handler.execute(command)

    async def test_local_auth_info_not_found(
        self, authenticate_command_handler, valid_user1, repositories
    ):
        """GIVEN: 유저는 있으나 LocalAuthInfo가 없을 때 WHEN: execute 호출 THEN: LocalAuthInfoNotFoundError가 발생한다."""
        # local_auth_info 저장소에서 해당 유저의 정보를 제거
        repositories["local_auth_info"].items = {}
        command = LocalUserAuthenticateCommand.create(
            now=datetime.now(),
            username=valid_user1.username.value,
            plain_password="Test_pw_1!",
        )
        with pytest.raises(LocalAuthInfoNotFoundError):
            await authenticate_command_handler.execute(command)
