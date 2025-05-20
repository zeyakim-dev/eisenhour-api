from dataclasses import dataclass
from datetime import timedelta, timezone
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column

from domain.base.entity import Entity
from infra.persistence.base.mapper import Mapper
from infra.persistence.sqlalchemy.base.model import SQLAlchemyModel
from infra.persistence.sqlalchemy.base.sqlalchemy_async_reposiotry import (
    SQLAlchemyAsyncRepository,
)
from shared_kernel.time.time_provider import TimeProvider

# --- 1) 엔진 & 세션팩토리 설정
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# --- 2) 테이블 생성 (한 번만)
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLAlchemyModel.metadata.drop_all)
        await conn.run_sync(SQLAlchemyModel.metadata.create_all)
    yield


# --- 3) SAVEPOINT 세션 격리
@pytest_asyncio.fixture
async def db_session(prepare_db):
    async with AsyncSessionLocal() as session:
        await session.begin()  # 최상위 트랜잭션
        await session.begin_nested()  # SAVEPOINT
        yield session
        await session.rollback()  # 롤백 → 데이터 초기화


class StubModel(SQLAlchemyModel):
    __tablename__ = "stub"

    name: Mapped[str] = mapped_column(String(255), nullable=False)


@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    name: str


class StubMapper(Mapper[StubEntity, StubModel]):
    def to_model(self, entity: StubEntity) -> StubModel:
        return StubModel(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self, model: StubModel) -> StubEntity:
        return StubEntity(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class StubRepository(SQLAlchemyAsyncRepository[StubEntity, StubModel]):
    def get_model_type(self) -> type[StubModel]:
        return StubModel


@pytest.fixture
def time_provider() -> TimeProvider:
    tz: timezone = timezone(timedelta(hours=9))
    return TimeProvider(tz=tz)


@pytest.fixture
def test_entity(time_provider: TimeProvider):
    return StubEntity.create(time_provider=time_provider, name="test")


@pytest_asyncio.fixture
async def stub_repository(
    db_session: AsyncSession, time_provider: TimeProvider, test_entity: StubEntity
) -> StubRepository:
    test_repository = StubRepository(db_session, StubMapper())
    db_session.add(test_entity)
    await db_session.flush()
    return test_repository


@pytest.mark.integration
@pytest.mark.asyncio
class TestSQLAlchemyAsyncRepository:
    async def test_commit_persists_data(
        self,
        db_session: AsyncSession,
        time_provider: TimeProvider,
        stub_repository: StubRepository,
        test_entity: StubEntity,
    ):
        new_model = StubModel(
            id=uuid4(),
            name="new",
            created_at=time_provider.now(),
            updated_at=time_provider.now(),
        )
        db_session.add(new_model)
        await stub_repository.commit()

        stmt = select(StubModel).where(StubModel.id == new_model.id)
        result = await db_session.execute(stmt)
        model = result.scalar_one()

        assert model.id == new_model.id
        assert model.name == new_model.name
        assert model.created_at == new_model.created_at
        assert model.updated_at == new_model.updated_at

    async def test_rollback_rolls_back_data(
        self,
        db_session: AsyncSession,
        time_provider: TimeProvider,
        stub_repository: StubRepository,
        test_entity: StubEntity,
    ):
        new_model = StubModel(
            id=uuid4(),
            name="new",
            created_at=time_provider.now(),
            updated_at=time_provider.now(),
        )
        db_session.add(new_model)
        await stub_repository.rollback()

        stmt = select(StubModel).where(StubModel.id == new_model.id)
        result = await db_session.execute(stmt)
        assert result.scalar_one_or_none() is None

    async def test_save(
        self,
        db_session: AsyncSession,
        time_provider: TimeProvider,
        stub_repository: StubRepository,
    ):
        entity = StubEntity.create(time_provider=time_provider, name="new")
        await stub_repository._save(entity)
        await db_session.flush()

        stmt = select(StubModel).where(StubModel.id == entity.id)
        result = await db_session.execute(stmt)
        model = result.scalar_one()

        assert model.id == entity.id
        assert model.name == entity.name
        assert model.created_at == entity.created_at.replace(tzinfo=None)
        assert model.updated_at == entity.updated_at.replace(tzinfo=None)

    async def test_get(self, stub_repository: StubRepository, test_entity: StubEntity):
        model = await stub_repository._get(test_entity.id)

        assert model.id == test_entity.id
        assert model.name == test_entity.name
        assert model.created_at == test_entity.created_at.replace(tzinfo=None)
        assert model.updated_at == test_entity.updated_at.replace(tzinfo=None)

    async def test_delete(
        self,
        db_session: AsyncSession,
        stub_repository: StubRepository,
        test_entity: StubEntity,
    ):
        await stub_repository._delete(test_entity.id)
        await db_session.flush()

        stmt = select(StubModel).where(StubModel.id == test_entity.id)
        result = await db_session.execute(stmt)
        assert result.scalar_one_or_none() is None
