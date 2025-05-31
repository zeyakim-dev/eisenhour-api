from sqlalchemy import select

from domain.auth.auth_info.google.google_auth_info import GoogleAuthInfo
from domain.auth.auth_info.google.repository.google_auth_info_repository import (
    GoogleAuthInfoRepository,
)
from domain.auth.auth_info.google.value_objects import GoogleSub
from infra.persistence.sqlalchemy.postgresql.auth_info.google.google_auth_info_model import (
    GoogleAuthInfoModel,
)
from infra.persistence.sqlalchemy.postgresql.base.pg_repository import (
    SQLAlchemyPGAsyncRepository,
)


class SQLAlchemyPGAsyncGoogleAuthInfoRepository(
    SQLAlchemyPGAsyncRepository[GoogleAuthInfo, GoogleAuthInfoModel],
    GoogleAuthInfoRepository,
):
    """
    PostgreSQL 기반 GoogleAuthInfo 저장소 구현체.

    - GoogleAuthInfoRepository 도메인 인터페이스를 PostgreSQL과 SQLAlchemy 기반으로 비동기 환경에서 구현합니다.
    - Google OAuth sub(고유 식별자)로 인증 정보를 조회할 수 있습니다.
    - 도메인 객체와 ORM 모델 간 매핑은 Mapper를 통해 처리합니다.
    - 기본 CRUD 및 트랜잭션 기능은 상위 SQLAlchemyPGAsyncRepository에서 제공합니다.

    Example:
        repo = SQLAlchemyPGAsyncGoogleAuthInfoRepository(session, mapper)
        auth_info = await repo._get_auth_info_by_sub(GoogleSub("sub-value"))
    """

    def get_model_type(self) -> type[GoogleAuthInfoModel]:
        """
        ORM 모델 타입을 반환합니다.

        Returns:
            type[GoogleAuthInfoModel]: GoogleAuthInfoModel 클래스 타입
        """
        return GoogleAuthInfoModel

    async def _get_auth_info_by_sub(self, sub: GoogleSub) -> GoogleAuthInfo | None:
        """
        GoogleSub(고유 식별자)로 GoogleAuthInfo를 조회합니다.

        Args:
            sub (GoogleSub): 조회할 Google OAuth sub 값

        Returns:
            GoogleAuthInfo | None: 조회된 인증 정보가 있으면 반환, 없으면 None
        """
        stmt = select(GoogleAuthInfoModel).where(GoogleAuthInfoModel.sub == sub.value)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self.mapper.to_entity(model)
