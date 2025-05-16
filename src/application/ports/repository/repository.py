from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from domain.base.entity import Entity

E = TypeVar("E", bound=Entity)


class Repository(ABC, Generic[E]):
    def save(self, entity: E) -> None:
        self._save(entity)

    @abstractmethod
    def _save(self, entity: E) -> None:
        pass

    def get(self, id: UUID) -> E:
        return self._get(id)

    @abstractmethod
    def _get(self, id: UUID) -> E:
        pass

    def delete(self, id: UUID) -> None:
        self._delete(id)

    @abstractmethod
    def _delete(self, id: UUID) -> None:
        pass
