from abc import abstractmethod

from application.ports.repository.repository import Repository
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from domain.user.user import User


class UserRepository(Repository[User]):
    def check_username_exists(self, username: str) -> None:
        if self._is_duplicate_username(username):
            raise UsernameAlreadyExistsError(username)

    def check_email_exists(self, email: str) -> None:
        if self._is_duplicate_email(email):
            raise EmailAlreadyExistsError(email)

    @abstractmethod
    def _is_duplicate_username(self, username: str) -> bool:
        pass

    @abstractmethod
    def _is_duplicate_email(self, email: str) -> bool:
        pass
