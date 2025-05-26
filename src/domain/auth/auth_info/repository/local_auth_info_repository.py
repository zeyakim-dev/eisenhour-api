from abc import abstractmethod
from uuid import UUID

from application.ports.repository.exceptions import EntityNotFoundError
from application.ports.repository.repository import AsyncRepository
from domain.auth.auth_info.local_auth_info import LocalAuthInfo


class LocalAuthInfoRepository(AsyncRepository[LocalAuthInfo]):
    async def get_user_auth_info(self, user_id: UUID) -> LocalAuthInfo:
        local_auth_info = await self._get_user_auth_info(user_id)
        if local_auth_info is None:
            raise EntityNotFoundError(
                repository_name=self.__class__.__name__, id=user_id
            )
        return local_auth_info

    @abstractmethod
    async def _get_user_auth_info(self, user_id: UUID) -> LocalAuthInfo | None: ...
