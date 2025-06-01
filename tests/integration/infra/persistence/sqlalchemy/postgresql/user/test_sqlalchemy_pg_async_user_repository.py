import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
)
from domain.user.user import User
from infra.persistence.sqlalchemy.postgresql.user.user_model import UserModel
from src.infra.persistence.sqlalchemy.postgresql.user.user_mapper import UserMapper
from src.infra.persistence.sqlalchemy.postgresql.user.user_repository import (
    SQLAlchemyPGAsyncUserRepository,
)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
engine = create_async_engine(DATABASE_URL, echo=False, future=True, poolclass=NullPool)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(UserModel.metadata.drop_all)
        await conn.run_sync(UserModel.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session(prepare_db):
    async with AsyncSessionLocal() as session:
        await session.begin()  # 외부 트랜잭션
        await session.begin_nested()  # SAVEPOINT
        yield session
        await session.rollback()  # 테스트 후 롤백


@pytest_asyncio.fixture
async def user_repository(
    test_user_model: UserModel, db_session: AsyncSession, user_mapper: UserMapper
):
    user_repository = SQLAlchemyPGAsyncUserRepository(
        session=db_session,
        mapper=user_mapper,
    )
    db_session.add(test_user_model)
    await db_session.flush()

    return user_repository


@pytest.mark.integration
@pytest.mark.asyncio
class TestSqlalchemyPgAsyncUserRepository:
    async def test_get_by_username_returns_user_when_exists(
        self,
        user_repository: SQLAlchemyPGAsyncUserRepository,
        test_user: User,
    ):
        user = await user_repository.get_by_username(test_user.username.value)
        assert user is not None
        assert user.username == test_user.username

    async def test_get_by_username_returns_none_when_not_exists(
        self,
        user_repository: SQLAlchemyPGAsyncUserRepository,
    ):
        new_username = "new_username"
        user = await user_repository.get_by_username(new_username)
        assert user is None

    async def test_check_email_exists_raise_exception_when_email_exists(
        self,
        user_repository: SQLAlchemyPGAsyncUserRepository,
        test_user: User,
    ):
        with pytest.raises(EmailAlreadyExistsError):
            await user_repository.check_email_exists(test_user.email.value)

    async def test_check_email_exists_returns_none_when_email_not_exists(
        self,
        user_repository: SQLAlchemyPGAsyncUserRepository,
    ):
        new_email = "new_email@test.com"
        assert await user_repository.check_email_exists(new_email) is None
