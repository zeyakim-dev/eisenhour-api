from dataclasses import dataclass

from application.messaging.command.base.command import Command
from application.messaging.command.base.command_handler import CommandResult


@dataclass(frozen=True, kw_only=True)
class UserRegisterCommand(Command):
    """사용자 등록을 위한 커맨드입니다.

    사용자명, 이메일, 평문 비밀번호를 포함하여 등록 요청을 전달합니다.

    Attributes:
        username (str): 등록할 사용자 이름.
        email (str): 등록할 이메일 주소.
        plain_password (str): 등록할 평문 비밀번호.
    """

    username: str
    email: str
    plain_password: str


@dataclass(frozen=True, kw_only=True)
class UserRegisterCommandResult(CommandResult):
    """사용자 등록 결과를 나타내는 커맨드 결과 객체입니다.

    등록된 사용자의 주요 정보를 포함합니다.

    Attributes:
        id (str): 생성된 사용자 식별자.
        username (str): 등록된 사용자 이름.
        email (str): 등록된 이메일 주소.
    """

    id: str
    username: str
    email: str
