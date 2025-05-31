from abc import abstractmethod

from application.ports.repository.repository import AsyncRepository
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
)
from domain.user.user import User


class UserRepository(AsyncRepository[User]):
    """비동기 환경에서 사용자 도메인 저장소를 정의하는 인터페이스입니다.

    사용자명 및 이메일 중복 검증 기능을 포함하며 기본 CRUD는 AsyncRepository
    에서 제공하는 메서드를 사용합니다.
    """

    async def get_by_username(self, username: str) -> User | None:
        """사용자명으로 사용자를 조회합니다.

        Args:
            username (str): 조회할 사용자명.
        """
        return await self._get_by_username(username)

    @abstractmethod
    async def _get_by_username(self, username: str) -> User | None:
        """사용자명으로 사용자를 조회합니다.

        Args:
            username (str): 조회할 사용자명.
        """
        ...

    async def check_email_exists(self, email: str) -> None:
        """이메일 중복 여부를 비동기 방식으로 검사합니다.

        Args:
            email (str): 중복 검사할 이메일 주소.

        Raises:
            EmailAlreadyExistsError: 중복된 이메일이 존재하는 경우 발생합니다.
        """
        if await self._is_duplicate_email(email):
            raise EmailAlreadyExistsError(email)

    @abstractmethod
    async def _is_duplicate_email(self, email: str) -> bool:
        """저장소에 이메일 중복 여부를 비동기 방식으로 확인합니다.

        Args:
            email (str): 검사할 이메일 주소.

        Returns:
            bool: 중복이면 True, 아니면 False.
        """
        ...
