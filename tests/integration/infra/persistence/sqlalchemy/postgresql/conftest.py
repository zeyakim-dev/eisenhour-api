from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from domain.auth.auth_info.local.local_auth_info import LocalAuthInfo
from domain.auth.auth_info.local.value_objects import HashedPassword
from domain.user.user import User
from domain.user.value_objects import Email, Username
from infra.persistence.sqlalchemy.postgresql.auth_info.local.local_auth_mapper import (
    LocalAuthInfoMapper,
)
from infra.persistence.sqlalchemy.postgresql.user.user_mapper import UserMapper

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
engine = create_async_engine(DATABASE_URL, echo=False, future=True, poolclass=NullPool)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session")
async def engine_fixture():
    return engine


@pytest_asyncio.fixture
async def db_session(engine_fixture):
    async with AsyncSessionLocal() as session:
        await session.begin()
        await session.begin_nested()
        yield session
        await session.rollback()


@pytest.fixture
def user_mapper():
    return UserMapper()


@pytest.fixture
def test_user():
    return User.create(
        now=datetime.now(),
        username=Username("test_user"),
        email=Email("test@test.com"),
    )


@pytest.fixture
def test_user_model(test_user, user_mapper):
    return user_mapper.to_model(test_user)


@pytest.fixture
def test_local_auth_info(test_user: User):
    return LocalAuthInfo.create(
        now=datetime.now(),
        user_id=test_user.id,
        hashed_password=HashedPassword("Hashed_pw_123!"),
    )


@pytest.fixture
def local_auth_info_mapper():
    return LocalAuthInfoMapper()


@pytest.fixture
def test_local_auth_info_model(
    test_local_auth_info: LocalAuthInfo, local_auth_info_mapper: LocalAuthInfoMapper
):
    return local_auth_info_mapper.to_model(test_local_auth_info)
