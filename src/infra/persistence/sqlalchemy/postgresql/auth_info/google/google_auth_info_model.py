from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infra.persistence.sqlalchemy.postgresql.base.pg_model import SQLAlchemyPGModel


class GoogleAuthInfoModel(SQLAlchemyPGModel):
    """
    구글 인증 정보의 SQLAlchemy ORM 모델.

    google_auth_infos 테이블에 매핑되며,
    사용자 ID(user_id), sub(고유 식별자), 프로필 이미지 URL(avatar_url)을 관리한다.

    Attributes:
        user_id (UUID): users 테이블의 외래 키, 각 사용자에 대한 고유 식별자.
        sub (str): Google OAuth의 sub(고유 식별자).
        avatar_url (str | None): 프로필 이미지 URL.
    """

    __tablename__ = "google_auth_infos"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    sub: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
