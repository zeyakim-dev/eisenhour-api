from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from domain.auth.auth_info.google.google_auth_info import GoogleAuthInfo
from domain.auth.auth_info.google.value_objects import GoogleSub
from domain.user.user import User
from infra.persistence.sqlalchemy.postgresql.auth_info.google.google_auth_info_model import (
    GoogleAuthInfoModel,
)
from infra.persistence.sqlalchemy.postgresql.auth_info.google.google_auth_info_repository import (
    SQLAlchemyPGAsyncGoogleAuthInfoRepository,
)
from infra.persistence.sqlalchemy.postgresql.auth_info.google.google_auth_mapper import (
    GoogleAuthInfoMapper,
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
        await conn.run_sync(GoogleAuthInfoModel.metadata.drop_all)
        await conn.run_sync(UserModel.metadata.drop_all)
        await conn.run_sync(GoogleAuthInfoModel.metadata.create_all)
        await conn.run_sync(UserModel.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session(prepare_db):
    async with AsyncSessionLocal() as session:
        await session.begin()
        await session.begin_nested()
        yield session
        await session.rollback()


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
def google_auth_info_mapper():
    return GoogleAuthInfoMapper()


@pytest.fixture
def test_google_auth_info(test_user: User):
    return GoogleAuthInfo.create(
        now=datetime.now(),
        user_id=test_user.id,
        sub=GoogleSub("test-google-sub"),
        avatar_url="https://example.com/avatar.png",
    )


@pytest_asyncio.fixture
def test_google_auth_info_model(
    test_google_auth_info: GoogleAuthInfo, google_auth_info_mapper: GoogleAuthInfoMapper
):
    return google_auth_info_mapper.to_model(test_google_auth_info)


@pytest_asyncio.fixture
async def google_auth_info_repository(
    test_google_auth_info_model,
    user_repository,
    db_session,
    google_auth_info_mapper,
):
    repo = SQLAlchemyPGAsyncGoogleAuthInfoRepository(
        session=db_session,
        mapper=google_auth_info_mapper,
    )
    db_session.add(test_google_auth_info_model)
    await db_session.flush()
    return repo


@pytest.mark.integration
@pytest.mark.asyncio
class TestSqlalchemyPgAsyncGoogleAuthInfoRepository:
    async def test_get_auth_info_by_sub_returns_google_auth_info_when_exists(
        self,
        google_auth_info_repository: SQLAlchemyPGAsyncGoogleAuthInfoRepository,
        test_google_auth_info: GoogleAuthInfo,
    ):
        """
        저장된 sub로 조회 시 GoogleAuthInfo가 반환되는지 검증합니다.
        """
        sub = test_google_auth_info.sub
        auth_info = await google_auth_info_repository.get_auth_info_by_sub(sub)
        assert auth_info is not None
        assert auth_info.sub.value == test_google_auth_info.sub.value
        assert auth_info.avatar_url == test_google_auth_info.avatar_url

    async def test_get_auth_info_by_sub_returns_none_when_not_exists(
        self,
        google_auth_info_repository: SQLAlchemyPGAsyncGoogleAuthInfoRepository,
    ):
        """
        존재하지 않는 sub로 조회 시 None이 반환되는지 검증합니다.
        """
        sub = GoogleSub("nonexisting-sub")
        auth_info = await google_auth_info_repository.get_auth_info_by_sub(sub)
        assert auth_info is None
