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
    """사용자 등록 요청을 처리하는 커맨드 핸들러.

    사용자명, 이메일 중복을 검증하고, 비밀번호를 해시한 뒤
    새 사용자 엔터티를 생성 및 저장한다. 생성 시각은 TimeProvider를 통해 설정된다.
    """

    def __init__(
        self, repository: UserRepository, time_provider: TimeProvider, hasher: Hasher
    ) -> None:
        """의존 객체를 주입받아 핸들러를 초기화한다.

        Args:
            repository (UserRepository): 사용자 저장소. 중복 검증과 저장 책임.
            time_provider (TimeProvider): 시간 정보를 제공. 생성 시간 설정에 사용.
            hasher (Hasher): 비밀번호 해시 및 검증을 수행.
        """
        self.repository = repository
        self.time_provider = time_provider
        self.hasher = hasher

    def execute(self, command: UserRegisterCommand) -> UserRegisterCommandResult:
        """사용자 등록 커맨드를 실행한다.

        사용자명, 이메일의 중복 여부를 확인하고, 비밀번호를 해시한다.
        생성된 사용자 엔터티는 저장소에 영속화되며, ID와 정보를 결과로 반환한다.

        Args:
            command (UserRegisterCommand): 사용자명, 이메일, 평문 비밀번호 포함.

        Returns:
            UserRegisterCommandResult: 생성된 사용자 ID, 이름, 이메일 정보.

        Raises:
            UsernameAlreadyExistsError: 사용자명이 이미 존재하는 경우.
            EmailAlreadyExistsError: 이메일이 이미 존재하는 경우.
        """
        username = Username(command.username)
        email = Email(command.email)
        plain_password = PlainPassword(command.plain_password)

        hashed_password_value = self.hasher.hash(plain_password.value)
        hashed_password = HashedPassword(hashed_password_value)

        self.repository.check_username_exists(username.value)
        self.repository.check_email_exists(email.value)

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
