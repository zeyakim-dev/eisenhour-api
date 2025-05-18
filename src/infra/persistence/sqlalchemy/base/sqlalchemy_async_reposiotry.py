from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.base.entity import Entity
from infra.persistence.base.mapper import Mapper, PersistenceModel

E = TypeVar("E", bound=Entity)
M = TypeVar("M", bound=PersistenceModel)


class ModelNotFoundError(Exception):
    """요청한 ID에 해당하는 모델을 찾을 수 없을 때 발생하는 예외입니다."""

    def __init__(self, model_name: str, id: UUID):
        """
        Args:
            model_name (str): 조회 실패한 모델 클래스 이름.
            id (UUID): 찾지 못한 엔터티의 식별자.
        """
        super().__init__(f"{model_name} with id {id} not found.")


class SQLAlchemyAsyncRepository(ABC, Generic[E, M]):
    """SQLAlchemy 기반 비동기 저장소 추상 클래스.

    도메인 엔터티와 ORM 모델 간 변환을 Mapper를 통해 처리하며,
    데이터베이스와 비동기 방식으로 상호작용하는 기본 저장소 기능을 제공합니다.

    Attributes:
        session (AsyncSession): SQLAlchemy 비동기 세션 인스턴스.
        mapper (Mapper): 도메인 엔터티와 ORM 모델 간 변환을 담당하는 매퍼.
    """

    def __init__(self, session: AsyncSession, mapper: Mapper[E, M]):
        """
        Args:
            session (AsyncSession): 비동기 DB 세션.
            mapper (Mapper): 엔터티-모델 변환기.
        """
        self.session = session
        self.mapper = mapper

    async def commit(self) -> None:
        """세션의 변경 사항을 커밋합니다.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: 커밋 실패 시 예외 발생 가능.
        """
        await self.session.commit()

    async def rollback(self) -> None:
        """세션의 변경 사항을 롤백합니다.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: 롤백 실패 시 예외 발생 가능.
        """
        await self.session.rollback()

    async def _save(self, entity: E) -> None:
        """도메인 엔터티를 ORM 모델로 변환 후 세션에 추가합니다.

        Args:
            entity (E): 저장할 도메인 엔터티.
        """
        model = self.mapper.to_model(entity)
        self.session.add(model)

    @abstractmethod
    def get_model_type(self) -> type[M]:
        """ORM 모델 클래스를 반환합니다.

        Returns:
            type[M]: 저장소가 다루는 ORM 모델 클래스.
        """
        ...

    async def _get(self, id: UUID) -> E:
        """주어진 ID로 ORM 모델을 조회하고 도메인 엔터티로 변환해 반환합니다.

        Args:
            id (UUID): 조회할 엔터티의 고유 식별자.

        Returns:
            E: 조회된 도메인 엔터티.

        Raises:
            ModelNotFoundError: 주어진 ID의 모델을 찾지 못했을 때.
        """
        model_cls: type[M] = self.get_model_type()
        stmt = select(model_cls).where(model_cls.id == id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise ModelNotFoundError(model_cls.__name__, id)

        return self.mapper.to_entity(model)

    async def _delete(self, id: UUID) -> None:
        """주어진 ID의 ORM 모델을 삭제합니다.

        Args:
            id (UUID): 삭제할 엔터티의 고유 식별자.
        """
        model_cls: type[M] = self.get_model_type()
        stmt = delete(model_cls).where(model_cls.id == id)
        await self.session.execute(stmt)
