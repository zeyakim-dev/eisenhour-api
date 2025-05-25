from dataclasses import dataclass
from datetime import datetime
from typing import Self

from domain.auth.auth_info.value_objects import HashedPassword
from domain.base.aggregate import Aggregate
from domain.user.value_objects import Email, PlainPassword, Username
from shared_kernel.hasher.hasher import Hasher


@dataclass(frozen=True, kw_only=True)
class User(Aggregate):
    """시스템의 사용자 정보를 표현하는 애그리거트 루트입니다.

    사용자명, 이메일, 해시된 비밀번호를 포함한 불변의 사용자 정보를 보유합니다.
    인증, 비밀번호 변경 등의 도메인 행위를 제공합니다.

    불변성을 유지하며, ID 및 타임스탬프는 Aggregate(Entity)로부터 상속됩니다.

    Attributes:
        username (Username): 사용자 식별용 고유 이름.
        email (Email): 사용자 이메일 주소.
        hashed_password (HashedPassword): 해시 처리된 사용자 비밀번호.
    """

    username: Username
    email: Email
    hashed_password: HashedPassword

    def authenticate(self, plain_password: PlainPassword, hasher: Hasher) -> bool:
        """입력된 평문 비밀번호로 인증을 수행합니다.

        Args:
            plain_password (PlainPassword): 사용자가 입력한 비밀번호.
            hasher (Hasher): 비밀번호 검증을 위한 해시 도구.

        Returns:
            bool: 인증 성공 여부. 일치하면 True, 그렇지 않으면 False.
        """
        return hasher.verify(plain_password.value, self.hashed_password.value)

    def change_password(
        self, now: datetime, plain_password: PlainPassword, hasher: Hasher
    ) -> Self:
        """비밀번호를 새 평문 비밀번호로 변경합니다.

        비밀번호는 내부에서 해시 처리되며, 변경 시 updated_at이 갱신됩니다.
        기존 인스턴스는 불변성을 유지하며 새로운 인스턴스를 반환합니다.

        Args:
            now (datetime): 비밀번호 변경 시간.
            plain_password (PlainPassword): 새 비밀번호(평문).
            hasher (Hasher): 비밀번호 해시에 사용되는 도구.

        Returns:
            Self: 비밀번호가 변경된 새로운 User 인스턴스.
        """
        new_hashed_password: HashedPassword = HashedPassword(
            hasher.hash(plain_password.value)
        )
        return self.update(now=now, hashed_password=new_hashed_password)
