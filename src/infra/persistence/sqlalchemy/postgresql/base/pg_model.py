from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from infra.persistence.sqlalchemy.base.model import SQLAlchemyModel


class SQLAlchemyPGModel(SQLAlchemyModel):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
