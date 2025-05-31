from abc import abstractmethod

from application.ports.repository.repository import AsyncRepository
from domain.auth.auth_info.google.google_auth_info import GoogleAuthInfo
from domain.auth.auth_info.google.value_objects import GoogleSub


class GoogleAuthInfoRepository(AsyncRepository[GoogleAuthInfo]):
    """
    GoogleAuthInfo 도메인용 비동기 저장소 인터페이스.

    GoogleSub(고유 식별자)로 인증 정보를 조회하는 책임을 가진다.
    기본 CRUD 메서드는 상위 AsyncRepository에서 제공한다.
    """

    async def get_auth_info_by_sub(self, sub: GoogleSub) -> GoogleAuthInfo | None:
        """
        GoogleSub(고유 식별자)로 GoogleAuthInfo를 조회한다.

        Args:
            sub (GoogleSub): 조회할 Google OAuth sub 값

        Returns:
            GoogleAuthInfo | None: 조회된 인증 정보가 있으면 반환, 없으면 None
        """
        google_auth_info = await self._get_auth_info_by_sub(sub)
        return google_auth_info

    @abstractmethod
    async def _get_auth_info_by_sub(self, sub: GoogleSub) -> GoogleAuthInfo | None:
        """
        저장소에서 GoogleSub로 GoogleAuthInfo를 조회한다.

        Args:
            sub (GoogleSub): 조회할 Google OAuth sub 값

        Returns:
            GoogleAuthInfo | None: 조회된 인증 정보가 있으면 반환, 없으면 None
        """
        ...
