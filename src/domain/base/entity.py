from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Any, Self
from uuid import UUID, uuid4

from domain.base.exceptions import TimestampRequiredError
from shared_kernel.time.time_provider import TimeProvider


@dataclass(frozen=True, kw_only=True)
class Entity:
    """도메인 엔터티의 기반 클래스입니다.

    각 엔터티는 고유한 UUID와 생성/수정 시각을 가지며,
    동등성 비교는 ID를 기준으로 이루어집니다.
    """

    id: UUID = field(default_factory=uuid4)
    created_at: datetime
    updated_at: datetime

    def __eq__(self, other: object) -> bool:
        """엔터티 간의 동등성 비교를 수행합니다.

        Args:
            other (object): 비교 대상 객체.

        Returns:
            bool: 두 엔터티의 ID가 같으면 True, 그렇지 않으면 False.
        """
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """엔터티의 해시 값을 반환합니다.

        Returns:
            int: 엔터티 ID를 기준으로 생성된 해시 값.
        """
        return hash(self.id)

    def __post_init__(self) -> None:
        """초기화 후 유효성 검사를 수행합니다.

        Raises:
            TimestampRequiredError: created_at 또는 updated_at이 None인 경우.
        """
        if self.created_at is None or self.updated_at is None:
            raise TimestampRequiredError()

    @classmethod
    def create(cls, time_provider: TimeProvider, **kwargs: Any) -> Self:
        """현재 시각을 기준으로 엔터티를 생성합니다.

        Args:
            time_provider (TimeProvider): 현재 시각을 제공하는 객체.
            **kwargs: 기타 엔터티 필드 값들.

        Returns:
            Self: 생성된 엔터티 인스턴스.
        """
        now = time_provider.now()
        kwargs.setdefault("created_at", now)
        kwargs.setdefault("updated_at", now)
        return cls(**kwargs)

    def update(self, time_provider: TimeProvider, **kwargs: Any) -> Self:
        """엔터티를 불변성을 유지한 채 업데이트합니다.

        Args:
            time_provider (TimeProvider): 현재 시각을 제공하는 객체.
            **kwargs: 수정할 필드 값들.

        Returns:
            Self: 수정된 엔터티 인스턴스.
        """
        now = time_provider.now()
        kwargs.setdefault("updated_at", now)
        return replace(self, **kwargs)
