from typing import TypedDict

from application.messaging.command.base.command_handler import CommandHandler
from application.messaging.command.user.user_register_command import (
    UserRegisterCommand,
    UserRegisterCommandResult,
)
from domain.auth.auth_info.base.value_objects import AuthType, AuthTypeEnum
from domain.auth.auth_info.local.local_auth_info import LocalAuthInfo
from domain.auth.auth_info.local.repository.local_auth_info_repository import (
    LocalAuthInfoRepository,
)
from domain.auth.auth_info.local.value_objects import HashedPassword, PlainPassword
from domain.user.repository.user_repository import UserRepository
from domain.user.user import User
from domain.user.value_objects import Email, Username
from shared_kernel.hasher.hasher import Hasher
from shared_kernel.time.time_provider import TimeProvider


class UserRegisterRepositories(TypedDict):
    user: UserRepository
    local_auth_info: LocalAuthInfoRepository


class UserRegisterCommandHandler(
    CommandHandler[UserRegisterCommand, UserRegisterCommandResult]
):
    """사용자 등록 요청을 처리하는 커맨드 핸들러.

    사용자명, 이메일 중복을 검증하고, 비밀번호를 해시한 뒤
    새 사용자 엔터티를 생성 및 저장한다. 생성 시각은 TimeProvider를 통해 설정된다.
    """

    def __init__(
        self,
        repositories: UserRegisterRepositories,
        time_provider: TimeProvider,
        hasher: Hasher,
    ) -> None:
        """의존 객체를 주입받아 핸들러를 초기화한다.

        Args:
            repository (UserRepository): 사용자 저장소. 중복 검증과 저장 책임.
            time_provider (TimeProvider): 시간 정보를 제공. 생성 시간 설정에 사용.
            hasher (Hasher): 비밀번호 해시 및 검증을 수행.
        """
        self.repositories = repositories
        self.time_provider = time_provider
        self.hasher = hasher

    async def execute(self, command: UserRegisterCommand) -> UserRegisterCommandResult:
        username = Username(command.username)
        email = Email(command.email)
        plain_password = PlainPassword(command.plain_password)

        hashed_password_value = self.hasher.hash(plain_password.value)
        hashed_password = HashedPassword(hashed_password_value)

        user_repository: UserRepository | None = self.repositories["user"]
        if not user_repository:
            raise ValueError()
        await user_repository.check_username_exists(username.value)
        await user_repository.check_email_exists(email.value)

        now = self.time_provider.now()

        user = User.create(
            now=now,
            username=username,
            email=email,
        )

        await user_repository.save(user)

        local_auth_info_repository: LocalAuthInfoRepository | None = self.repositories[
            "local_auth_info"
        ]
        if not local_auth_info_repository:
            raise ValueError()
        local_auth_info = LocalAuthInfo.create(
            now=now,
            user_id=user.id,
            auth_type=AuthType(AuthTypeEnum.LOCAL),
            hashed_password=hashed_password,
        )
        await local_auth_info_repository.save(local_auth_info)

        return UserRegisterCommandResult(
            id=str(user.id),
            username=user.username.value,
            email=user.email.value,
            auth_type=AuthTypeEnum.LOCAL.value,
        )
