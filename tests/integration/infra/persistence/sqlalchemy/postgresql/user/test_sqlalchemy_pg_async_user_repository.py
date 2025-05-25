from datetime import timedelta, timezone

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from domain.auth.auth_info.value_objects import HashedPassword
from domain.user.repository.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from domain.user.user import User
from domain.user.value_objects import Email, Username
from infra.persistence.sqlalchemy.postgresql.user.user_model import UserModel
from shared_kernel.time.time_provider import TimeProvider
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


@pytest.fixture
def time_provider():
    tz_kst = timezone(timedelta(hours=9))
    return TimeProvider(tz_kst)


@pytest.fixture
def user_mapper():
    return UserMapper()


@pytest.fixture
def test_user(time_provider: TimeProvider):
    return User.create(
        time_provider=time_provider,
        username=Username("test_user"),
        email=Email("test@test.com"),
        hashed_password=HashedPassword("Test_pw_123!"),
    )


@pytest.fixture
def test_user_model(test_user: User, user_mapper: UserMapper):
    return user_mapper.to_model(test_user)


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
    async def test_check_username_exists_raise_exception_when_username_exists(
        self,
        user_repository: SQLAlchemyPGAsyncUserRepository,
        test_user: User,
    ):
        with pytest.raises(UsernameAlreadyExistsError):
            await user_repository.check_username_exists(test_user.username.value)

    async def test_check_username_exists_returns_none_when_username_not_exists(
        self,
        user_repository: SQLAlchemyPGAsyncUserRepository,
    ):
        new_username = "new_username"
        assert await user_repository.check_username_exists(new_username) is None

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
