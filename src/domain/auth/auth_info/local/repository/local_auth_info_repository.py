from abc import abstractmethod
from uuid import UUID

from application.ports.repository.repository import AsyncRepository
from domain.auth.auth_info.local.local_auth_info import LocalAuthInfo
from domain.auth.auth_info.local.repository.exceptions import LocalAuthInfoNotFoundError


class LocalAuthInfoRepository(AsyncRepository[LocalAuthInfo]):
    """LocalAuthInfo 도메인용 비동기 저장소 인터페이스.

    사용자 ID를 기준으로 인증 정보를 조회하는 책임을 가진다.
    기본 CRUD 메서드는 상위 AsyncRepository에서 제공한다.
    """

    async def get_user_auth_info(self, user_id: UUID) -> LocalAuthInfo:
        """사용자 ID로 LocalAuthInfo를 조회한다.

        Args:
            user_id (UUID): 조회할 사용자 ID.

        Returns:
            LocalAuthInfo: 조회된 사용자 인증 정보.

        Raises:
            EntityNotFoundError: 해당 사용자 ID의 인증 정보가 존재하지 않을 때 발생한다.
        """
        local_auth_info = await self._get_user_auth_info(user_id)
        if local_auth_info is None:
            raise LocalAuthInfoNotFoundError(str(user_id))
        return local_auth_info

    @abstractmethod
    async def _get_user_auth_info(self, user_id: UUID) -> LocalAuthInfo | None:
        """저장소에서 사용자 ID로 LocalAuthInfo를 조회한다.

        Args:
            user_id (UUID): 조회할 사용자 ID.

        Returns:
            LocalAuthInfo | None: 조회된 인증 정보가 있으면 반환하고, 없으면 None.
        """
        ...
