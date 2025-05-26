from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infra.persistence.sqlalchemy.postgresql.base.pg_model import SQLAlchemyPGModel


class LocalAuthInfoModel(SQLAlchemyPGModel):
    """로컬 인증 정보의 SQLAlchemy ORM 모델.

    local_auth_infos 테이블에 매핑되며,
    사용자 ID(user_id)와 해시된 비밀번호(hashed_password)를 관리한다.

    Attributes:
        user_id (UUID): users 테이블의 외래 키, 각 사용자에 대한 고유 식별자.
        hashed_password (str): 해시된 비밀번호 값.
    """

    __tablename__ = "local_auth_infos"

    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    password_expired_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
