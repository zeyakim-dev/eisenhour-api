from uuid import UUID

from sqlalchemy import select

from domain.auth.auth_info.local_auth_info import LocalAuthInfo
from domain.auth.auth_info.repository.local_auth_info_repository import (
    LocalAuthInfoRepository,
)
from infra.persistence.sqlalchemy.postgresql.auth_info.local_auth_info.local_auth_info_model import (
    LocalAuthInfoModel,
)
from infra.persistence.sqlalchemy.postgresql.base.pg_repository import (
    SQLAlchemyPGAsyncRepository,
)


class LocalAuthInfoPGAsyncRepository(
    SQLAlchemyPGAsyncRepository[LocalAuthInfo, LocalAuthInfoModel],
    LocalAuthInfoRepository,
):
    """PostgreSQL 기반 LocalAuthInfo 저장소 구현체.

    LocalAuthInfoRepository 인터페이스를 PostgreSQL과 SQLAlchemy 기반으로
    비동기 환경에서 구현한다.

    Methods:
        get_model_type: ORM 모델 클래스를 반환한다.
        _get_user_auth_info: 사용자 ID로 인증 정보를 조회한다.
    """

    def get_model_type(self) -> type[LocalAuthInfoModel]:
        """ORM 모델 타입을 반환한다.

        Returns:
            type[LocalAuthInfoModel]: LocalAuthInfoModel 클래스 타입.
        """
        return LocalAuthInfoModel

    async def _get_user_auth_info(self, user_id: UUID) -> LocalAuthInfo | None:
        """사용자 ID로 LocalAuthInfo를 조회한다.

        Args:
            user_id (UUID): 조회할 사용자 ID.

        Returns:
            LocalAuthInfo | None: 조회된 인증 정보 엔터티. 없으면 None.
        """
        stmt = select(LocalAuthInfoModel).where(LocalAuthInfoModel.user_id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self.mapper.to_entity(model)
