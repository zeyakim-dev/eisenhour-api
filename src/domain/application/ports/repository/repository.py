from abc import ABC, abstractmethod
from uuid import UUID

from domain.base.entity import Entity


class Repository(ABC):
    def save(self, entity: Entity) -> None:
        self._save(entity)

    @abstractmethod
    def _save(self, entity: Entity) -> None:
        pass

    def get(self, id: UUID) -> Entity:
        return self._get(id)

    @abstractmethod
    def _get(self, id: UUID) -> Entity:
        pass

    def delete(self, id: UUID) -> None:
        self._delete(id)

    @abstractmethod
    def _delete(self, id: UUID) -> None:
        pass
