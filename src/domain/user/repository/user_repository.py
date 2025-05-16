from abc import abstractmethod

from application.ports.repository.repository import Repository
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from domain.user.user import User


class UserRepository(Repository[User]):
    """사용자 도메인에 특화된 저장소 인터페이스입니다.

    사용자명과 이메일의 중복 검증 기능을 포함하며,
    기본 CRUD 기능은 상위 Repository 클래스에서 제공합니다.
    """

    def check_username_exists(self, username: str) -> None:
        """사용자 이름 중복 여부를 검사합니다.

        Args:
            username (str): 중복 검사할 사용자 이름.

        Raises:
            UsernameAlreadyExistsError: 중복된 사용자 이름이 존재하는 경우 발생합니다.
        """
        if self._is_duplicate_username(username):
            raise UsernameAlreadyExistsError(username)

    def check_email_exists(self, email: str) -> None:
        """이메일 중복 여부를 검사합니다.

        Args:
            email (str): 중복 검사할 이메일 주소.

        Raises:
            EmailAlreadyExistsError: 중복된 이메일이 존재하는 경우 발생합니다.
        """
        if self._is_duplicate_email(email):
            raise EmailAlreadyExistsError(email)

    @abstractmethod
    def _is_duplicate_username(self, username: str) -> bool:
        """저장소에 사용자 이름 중복 여부를 확인합니다.

        Args:
            username (str): 검사할 사용자 이름.

        Returns:
            bool: 중복이면 True, 아니면 False.
        """
        pass

    @abstractmethod
    def _is_duplicate_email(self, email: str) -> bool:
        """저장소에 이메일 중복 여부를 확인합니다.

        Args:
            email (str): 검사할 이메일 주소.

        Returns:
            bool: 중복이면 True, 아니면 False.
        """
        pass
