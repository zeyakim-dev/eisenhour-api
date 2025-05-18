from abc import ABC, abstractmethod
from typing import Any, Generic, Protocol, TypeVar

from domain.base.entity import Entity


class PersistenceModel(Protocol):
    """저장소에서 사용하는 영속화 모델의 최소 인터페이스입니다.

    영속화 모델은 고유 식별자인 `id` 필드를 필수로 포함해야 합니다.
    주로 ORM 모델(SQLAlchemy 등)이 이 프로토콜을 구현하게 됩니다.
    """

    id: Any


E = TypeVar("E", bound=Entity)
M = TypeVar("M", bound=PersistenceModel)


class Mapper(ABC, Generic[E, M]):
    """도메인 엔터티와 영속화 모델 간 매핑을 정의하는 추상 클래스입니다.

    저장소 구현에서 도메인 엔티티와 ORM 모델 간 변환 책임을 분리하기 위해 사용됩니다.
    이 클래스를 상속받는 구체 매퍼는 엔티티와 모델 간 1:1 변환 규칙을 제공합니다.
    """

    @abstractmethod
    def to_model(self, entity: E) -> M:
        """도메인 엔티티를 영속화 모델로 변환합니다.

        Args:
            entity (E): 변환할 도메인 엔터티.

        Returns:
            M: 해당 도메인 엔터티에 대응하는 ORM 모델 또는 영속 객체.
        """
        ...

    @abstractmethod
    def to_entity(self, model: M) -> E:
        """영속화 모델을 도메인 엔터티로 변환합니다.

        Args:
            model (M): 변환할 ORM 모델 또는 영속 객체.

        Returns:
            E: 해당 모델에 대응하는 도메인 엔터티.
        """
        ...
