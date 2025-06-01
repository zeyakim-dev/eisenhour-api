from typing import TypedDict

from application.messaging.command.auth.local.handler.exceptions import (
    WrongPasswordError,
)
from application.messaging.command.auth.local.local_user_authenticate_command import (
    LocalUserAuthenticateCommand,
    LocalUserAuthenticateCommandResult,
)
from application.messaging.command.base.command_handler import CommandHandler
from application.messaging.command.base.exceptions import RepositoryNotFoundError
from application.ports.jwt_provider.jwt_provider import JWTProvider
from domain.auth.auth_info.local.repository.exceptions import LocalAuthInfoNotFoundError
from domain.auth.auth_info.local.repository.local_auth_info_repository import (
    LocalAuthInfoRepository,
)
from domain.auth.auth_info.local.value_objects import PlainPassword
from domain.user.repository.exceptions import UsernameNotFoundError
from domain.user.repository.user_repository import UserRepository
from domain.user.value_objects import Username
from shared_kernel.hasher.hasher import Hasher


class LocalUserAuthenticateRepositories(TypedDict):
    user: UserRepository
    local_auth_info: LocalAuthInfoRepository


class LocalUserAuthenticateCommandHandler(
    CommandHandler[LocalUserAuthenticateCommand, LocalUserAuthenticateCommandResult]
):
    """
    Local 인증(로그인) 요청을 처리하는 커맨드 핸들러의 원형입니다.
    """

    def __init__(
        self,
        repositories: LocalUserAuthenticateRepositories,
        hasher: Hasher,
        jwt_provider: JWTProvider,
    ):
        self.repositories = repositories
        self.hasher = hasher
        self.jwt_provider = jwt_provider

    async def execute(
        self, command: LocalUserAuthenticateCommand
    ) -> LocalUserAuthenticateCommandResult:
        """
        Local 인증(로그인) 요청을 처리합니다.
        (구체 구현은 이후 작성)
        """
        username = Username(command.username)
        plain_password = PlainPassword(command.plain_password)

        user_repository: UserRepository | None = self.repositories.get("user")
        if not user_repository:
            raise RepositoryNotFoundError("user")
        local_auth_info_repository: LocalAuthInfoRepository | None = (
            self.repositories.get("local_auth_info")
        )
        if not local_auth_info_repository:
            raise RepositoryNotFoundError("local_auth_info")

        user = await user_repository.get_by_username(username.value)
        if not user:
            raise UsernameNotFoundError(username.value)

        local_auth_info = await local_auth_info_repository.get_user_auth_info(user.id)
        if not local_auth_info:
            raise LocalAuthInfoNotFoundError(str(user.id))

        if not self.hasher.verify(
            plain_password.value, local_auth_info.hashed_password.value
        ):
            raise WrongPasswordError(username.value)

        payload = {
            "id": str(user.id),
            "email": user.email.value,
            "username": user.username.value,
        }

        access_payload = payload.copy()
        access_payload["type"] = "access"
        refresh_payload = payload.copy()
        refresh_payload["type"] = "refresh"
        access_token = self.jwt_provider.encode(
            access_payload, expires_in=60 * 60 * 24 * 14
        )
        refresh_token = self.jwt_provider.encode(
            refresh_payload, expires_in=60 * 60 * 24 * 14 * 14
        )

        return LocalUserAuthenticateCommandResult(
            id=str(user.id),
            email=user.email.value,
            username=user.username.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
            access_token=access_token,
            refresh_token=refresh_token,
        )
