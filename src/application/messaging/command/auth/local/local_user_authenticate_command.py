from dataclasses import dataclass
from datetime import datetime

from application.messaging.command.base.command import Command
from application.messaging.command.base.command_handler import CommandResult


@dataclass(frozen=True, kw_only=True)
class LocalUserAuthenticateCommand(Command):
    """
    Local 인증(로그인) 요청을 위한 커맨드입니다.

    Attributes:
        username (str): 로그인 시도할 사용자명
        plain_password (str): 평문 비밀번호
    """

    username: str
    plain_password: str


@dataclass(frozen=True, kw_only=True)
class LocalUserAuthenticateCommandResult(CommandResult):
    """
    Local 인증(로그인) 결과를 나타내는 커맨드 결과 객체입니다.

    Attributes:
        user_id (str): 인증된 사용자 식별자
        access_token (str): 인증 성공 시 발급된 액세스 토큰(JWT 등)
        refresh_token (str | None): 리프레시 토큰(필요시)
    """

    id: str
    email: str
    username: str
    created_at: datetime
    updated_at: datetime
    access_token: str
    refresh_token: str | None = None
