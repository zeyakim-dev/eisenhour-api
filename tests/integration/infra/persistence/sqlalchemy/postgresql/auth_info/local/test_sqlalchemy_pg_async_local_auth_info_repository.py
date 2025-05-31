from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from application.ports.repository.exceptions import EntityNotFoundError
from domain.auth.auth_info.local.local_auth_info import LocalAuthInfo
from infra.persistence.sqlalchemy.postgresql.auth_info.local.local_auth_info_model import (
    LocalAuthInfoModel,
)
from infra.persistence.sqlalchemy.postgresql.auth_info.local.local_auth_info_repository import (
    SQLAlchemyPGAsyncLocalAuthInfoRepository,
)
from infra.persistence.sqlalchemy.postgresql.auth_info.local.local_auth_mapper import (
    LocalAuthInfoMapper,
)
from infra.persistence.sqlalchemy.postgresql.user.user_mapper import UserMapper
from infra.persistence.sqlalchemy.postgresql.user.user_model import UserModel
from infra.persistence.sqlalchemy.postgresql.user.user_repository import (
    SQLAlchemyPGAsyncUserRepository,
)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
engine = create_async_engine(DATABASE_URL, echo=False, future=True, poolclass=NullPool)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(LocalAuthInfoModel.metadata.drop_all)
        await conn.run_sync(UserModel.metadata.drop_all)
        await conn.run_sync(LocalAuthInfoModel.metadata.create_all)
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


@pytest_asyncio.fixture
async def local_auth_info_repository(
    test_local_auth_info_model: LocalAuthInfoModel,
    user_repository: SQLAlchemyPGAsyncUserRepository,
    db_session: AsyncSession,
    local_auth_info_mapper: LocalAuthInfoMapper,
):
    local_auth_info_repository = SQLAlchemyPGAsyncLocalAuthInfoRepository(
        session=db_session,
        mapper=local_auth_info_mapper,
    )
    db_session.add(test_local_auth_info_model)
    await db_session.flush()

    return local_auth_info_repository


@pytest.mark.integration
@pytest.mark.asyncio
class TestSqlalchemyPgAsyncLocalAuthInfoRepository:
    async def test_get_user_auth_info_returns_local_auth_info_when_user_exists(
        self,
        local_auth_info_repository: SQLAlchemyPGAsyncLocalAuthInfoRepository,
        test_local_auth_info: LocalAuthInfo,
    ):
        local_auth_info = await local_auth_info_repository.get_user_auth_info(
            test_local_auth_info.user_id
        )
        assert local_auth_info == test_local_auth_info

    async def test_get_user_auth_info_raise_exception_when_user_not_exists(
        self,
        local_auth_info_repository: SQLAlchemyPGAsyncLocalAuthInfoRepository,
    ):
        nonexisting_user_id = uuid4()
        with pytest.raises(EntityNotFoundError):
            await local_auth_info_repository.get_user_auth_info(nonexisting_user_id)
