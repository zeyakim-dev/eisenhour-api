from typing import TypeVar

from domain.base.entity import Entity
from infra.persistence.sqlalchemy.base.model import SQLAlchemyModel
from infra.persistence.sqlalchemy.base.sqlalchemy_async_reposiotry import (
    SQLAlchemyAsyncRepository,
)

E = TypeVar("E", bound=Entity)
M = TypeVar("M", bound=SQLAlchemyModel)


class SQLAlchemyPGAsyncRepository(SQLAlchemyAsyncRepository[E, M]):
    pass
