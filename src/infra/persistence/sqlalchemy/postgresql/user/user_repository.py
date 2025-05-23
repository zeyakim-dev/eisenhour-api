from sqlalchemy import select

from domain.user.repository.user_repository import UserRepository
from domain.user.user import User
from infra.persistence.sqlalchemy.postgresql.base.pg_repository import (
    SQLAlchemyPGAsyncRepository,
)
from infra.persistence.sqlalchemy.postgresql.user.user_model import UserModel


class SQLAlchemyPGAsyncUserRepository(
    SQLAlchemyPGAsyncRepository[User, UserModel], UserRepository
):
    def get_model_type(self) -> type[UserModel]:
        return UserModel

    async def _is_duplicate_username(self, username: str) -> bool:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def _is_duplicate_email(self, email: str) -> bool:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
