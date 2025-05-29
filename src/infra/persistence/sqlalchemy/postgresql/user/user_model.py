from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infra.persistence.sqlalchemy.postgresql.base.pg_model import SQLAlchemyPGModel


class UserModel(SQLAlchemyPGModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
