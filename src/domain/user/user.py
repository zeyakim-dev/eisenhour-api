from dataclasses import dataclass

from domain.base.aggregate import Aggregate
from domain.user.value_objects import Email, Username


@dataclass(frozen=True, kw_only=True)
class User(Aggregate):
    """시스템의 사용자 정보를 표현하는 애그리거트 루트입니다.

    사용자명과 이메일을 포함한 불변의 사용자 정보를 보유합니다.
    인증, 비밀번호 변경 등의 도메인 행위는 별도의 책임으로 분리되어 있습니다.

    Attributes:
        username (Username): 사용자 식별용 고유 이름.
        email (Email): 사용자 이메일 주소.
    """

    username: Username
    email: Email
