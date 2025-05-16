"""도메인 엔터티 저장소 추상 클래스 모듈입니다.

Repository는 도메인 엔터티의 저장, 조회, 삭제와 같은 영속성 관련 동작을 정의합니다.
구체 구현은 하위 클래스에서 제공하며, 인터페이스 수준에서 일관된 계약을 제공합니다.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from domain.base.entity import Entity

E = TypeVar("E", bound=Entity)


class Repository(ABC, Generic[E]):
    """도메인 엔터티를 관리하는 저장소의 추상 기반 클래스입니다.

    저장소는 Entity의 영속화 로직을 캡슐화하며, 도메인 로직과 인프라를 분리합니다.
    구체 저장 방식은 하위 클래스에서 구현합니다.
    """

    def save(self, entity: E) -> None:
        """엔터티를 저장하거나 갱신합니다.

        Args:
            entity (E): 저장 대상 도메인 엔터티.
        """
        self._save(entity)

    @abstractmethod
    def _save(self, entity: E) -> None:
        """저장 또는 갱신 로직의 구체 구현을 제공합니다.

        Args:
            entity (E): 저장할 도메인 엔터티.
        """
        pass

    def get(self, id: UUID) -> E:
        """식별자를 통해 엔터티를 조회합니다.

        Args:
            id (UUID): 조회할 엔터티의 고유 식별자.

        Returns:
            E: 조회된 도메인 엔터티. 존재하지 않을 경우 예외를 발생시킬 수 있습니다.
        """
        return self._get(id)

    @abstractmethod
    def _get(self, id: UUID) -> E:
        """엔터티 조회 로직의 구체 구현을 제공합니다.

        Args:
            id (UUID): 조회할 엔터티의 식별자.

        Returns:
            E: 조회된 도메인 엔터티.
        """
        pass

    def delete(self, id: UUID) -> None:
        """식별자를 기반으로 엔터티를 삭제합니다.

        Args:
            id (UUID): 삭제할 엔터티의 고유 식별자.
        """
        self._delete(id)

    @abstractmethod
    def _delete(self, id: UUID) -> None:
        """엔터티 삭제 로직의 구체 구현을 제공합니다.

        Args:
            id (UUID): 삭제할 엔터티의 식별자.
        """
        pass
