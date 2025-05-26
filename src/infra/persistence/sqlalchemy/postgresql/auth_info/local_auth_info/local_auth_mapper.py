from domain.auth.auth_info.local_auth_info import LocalAuthInfo
from domain.auth.auth_info.value_objects import HashedPassword
from infra.persistence.base.mapper import Mapper
from infra.persistence.sqlalchemy.postgresql.auth_info.local_auth_info.local_auth_info_model import (
    LocalAuthInfoModel,
)


class LocalAuthInfoMapper(Mapper[LocalAuthInfo, LocalAuthInfoModel]):
    """LocalAuthInfo 엔터티와 LocalAuthInfoModel 간 매핑을 수행하는 매퍼 클래스."""

    def to_entity(self, model: LocalAuthInfoModel) -> LocalAuthInfo:
        return LocalAuthInfo(
            id=model.id,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            hashed_password=HashedPassword(model.hashed_password),
            password_expired_at=model.password_expired_at,
        )

    def to_model(self, entity: LocalAuthInfo) -> LocalAuthInfoModel:
        return LocalAuthInfoModel(
            id=entity.id,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            hashed_password=entity.hashed_password.value,
            password_expired_at=entity.password_expired_at,
        )
