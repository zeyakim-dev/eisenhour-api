from domain.auth.auth_info.google.google_auth_info import GoogleAuthInfo
from domain.auth.auth_info.google.value_objects import GoogleSub
from infra.persistence.base.mapper import Mapper
from infra.persistence.sqlalchemy.postgresql.auth_info.google.google_auth_info_model import (
    GoogleAuthInfoModel,
)


class GoogleAuthInfoMapper(Mapper[GoogleAuthInfo, GoogleAuthInfoModel]):
    """
    GoogleAuthInfo 도메인 객체와 GoogleAuthInfoModel ORM 모델 간 매핑을 수행하는 매퍼 클래스.
    """

    def to_entity(self, model: GoogleAuthInfoModel) -> GoogleAuthInfo:
        return GoogleAuthInfo(
            id=model.id,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            sub=GoogleSub(model.sub),
            avatar_url=model.avatar_url,
        )

    def to_model(self, entity: GoogleAuthInfo) -> GoogleAuthInfoModel:
        return GoogleAuthInfoModel(
            id=entity.id,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            sub=entity.sub.value,
            avatar_url=entity.avatar_url,
        )
