from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 Declarative Base 클래스.

    모든 ORM 모델의 기반이 되는 추상 베이스 클래스입니다.
    메타데이터 및 선언적 구성을 위한 공통 기반을 제공합니다.
    """


class SQLAlchemyModel(Base):
    """모든 영속성 모델이 상속하는 추상 기반 클래스.

    공통 식별자(id) 및 생성/수정 시간 필드를 정의합니다.
    id와 시간 필드는 도메인 계층에서 주입되어야 하며,
    이 클래스는 해당 값을 단순 저장하는 역할만 수행합니다.

    Attributes:
        id (UUID): 모델의 고유 식별자.
        created_at (datetime): 모델이 최초 생성된 시간.
        updated_at (datetime): 모델이 마지막으로 수정된 시간.
    """

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
