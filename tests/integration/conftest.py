import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from infra.persistence.sqlalchemy.base.model import Base

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session")
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session(prepare_db):
    async with AsyncSessionLocal() as session:
        # 최상위 트랜잭션 시작
        await session.begin()
        # SAVEPOINT 생성
        await session.begin_nested()
        yield session
        # 각 테스트 끝나면 SAVEPOINT 롤백 → 변경사항 없던 것처럼
        await session.rollback()
