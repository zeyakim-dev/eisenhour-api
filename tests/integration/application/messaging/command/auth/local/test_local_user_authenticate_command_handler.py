from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from application.messaging.command.auth.local.handler.local_user_authenticate_command_handler import (
    LocalUserAuthenticateCommandHandler,
)
from application.messaging.command.auth.local.local_user_authenticate_command import (
    LocalUserAuthenticateCommand,
)
from domain.auth.auth_info.local.repository.exceptions import LocalAuthInfoNotFoundError
from domain.user.repository.exceptions import UsernameNotFoundError
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
from infra.security.jwt_provider.py_jwt_provider import PyJWTProvider
from shared_kernel.time.time_provider import TimeProvider

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


@pytest.fixture
def repositories(user_repository, local_auth_info_repository):
    return {
        "user": user_repository,
        "local_auth_info": local_auth_info_repository,
    }


@pytest.fixture
def time_provider():
    kst = timezone(timedelta(hours=9))
    return TimeProvider(kst)


@pytest.fixture
def jwt_provider(time_provider):
    return PyJWTProvider(time_provider=time_provider, secret="test_secret")


@pytest.fixture
def handler(repositories, hasher, jwt_provider):
    return LocalUserAuthenticateCommandHandler(
        repositories=repositories,
        hasher=hasher,
        jwt_provider=jwt_provider,
    )


@pytest.mark.integration
@pytest.mark.asyncio
class TestLocalUserAuthenticateCommandIntegration:
    async def test_successful_authentication(
        self, handler, test_user, test_local_auth_info, jwt_provider
    ):
        """GIVEN: 실제 DB에 유저/LocalAuthInfo가 존재 WHEN: 올바른 username, password로 로그인 THEN: 토큰 및 사용자 정보 반환"""
        command = LocalUserAuthenticateCommand.create(
            now=datetime.now(),
            username=test_user.username.value,
            plain_password="Password_123!",
        )
        result = await handler.execute(command)
        assert result.username == test_user.username.value
        assert result.email == test_user.email.value

        payload = jwt_provider.decode(result.access_token)
        assert payload["username"] == test_user.username.value
        assert payload["type"] == "access"

    async def test_wrong_password(self, handler, test_user):
        """GIVEN: 올바르지 않은 password WHEN: 로그인 시도 THEN: WrongPasswordError 발생"""
        command = LocalUserAuthenticateCommand.create(
            now=datetime.now(),
            username=test_user.username.value,
            plain_password="Wrong_pw_123!",
        )
        from application.messaging.command.auth.local.handler.exceptions import (
            WrongPasswordError,
        )

        with pytest.raises(WrongPasswordError):
            await handler.execute(command)

    async def test_nonexistent_user(self, handler):
        """GIVEN: 존재하지 않는 username WHEN: 로그인 시도 THEN: UsernameNotFoundError 발생"""
        command = LocalUserAuthenticateCommand.create(
            now=datetime.now(),
            username="not_exist_user",
            plain_password="Irrelevant_pw_123!",
        )
        with pytest.raises(UsernameNotFoundError):
            await handler.execute(command)

    async def test_local_auth_info_not_found(self, handler, test_user):
        """GIVEN: 유저는 있으나 LocalAuthInfo가 없는 경우 WHEN: 로그인 시도 THEN: LocalAuthInfoNotFoundError 발생"""

        auth_info = await handler.repositories["local_auth_info"].get_user_auth_info(
            test_user.id
        )
        await handler.repositories["local_auth_info"].delete(auth_info.id)
        command = LocalUserAuthenticateCommand.create(
            now=datetime.now(),
            username=test_user.username.value,
            plain_password="Password_123!",
        )
        with pytest.raises(LocalAuthInfoNotFoundError):
            await handler.execute(command)
