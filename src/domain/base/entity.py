from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Any, Self
from uuid import UUID, uuid4

from domain.base.exceptions import TimestampRequiredError


@dataclass(frozen=True, kw_only=True)
class Entity:
    """도메인 엔터티의 기반 클래스입니다.

    각 엔터티는 고유한 UUID와 생성/수정 시각을 가지며,
    동등성 비교는 ID를 기준으로 수행됩니다.
    """

    id: UUID = field(default_factory=uuid4)
    created_at: datetime
    updated_at: datetime

    def __eq__(self, other: object) -> bool:
        """엔터티 간의 동등성 비교를 수행합니다.

        Args:
            other (object): 비교 대상 객체입니다.

        Returns:
            bool: 두 엔터티의 ID가 같으면 True를 반환합니다.
        """
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """엔터티의 해시 값을 반환합니다.

        Returns:
            int: 엔터티 ID를 기준으로 생성된 해시 값입니다.
        """
        return hash(self.id)

    def __post_init__(self) -> None:
        """초기화 후 유효성 검사를 수행합니다.

        created_at 또는 updated_at이 None인 경우 예외를 발생시킵니다.

        Raises:
            TimestampRequiredError: 타임스탬프가 지정되지 않은 경우 발생합니다.
        """
        if self.created_at is None or self.updated_at is None:
            raise TimestampRequiredError()

    @classmethod
    def create(cls, now: datetime, **kwargs: Any) -> Self:
        """현재 시각을 기준으로 엔터티를 생성합니다.

        Args:
            now (datetime): 생성 시각.
            **kwargs: 엔터티 생성에 필요한 기타 필드 값입니다.

        Returns:
            Self: 생성된 엔터티 인스턴스를 반환합니다.
        """
        kwargs.update({"created_at": now, "updated_at": now})
        return cls(**kwargs)

    def update(self, now: datetime, **kwargs: Any) -> Self:
        """엔터티를 불변성을 유지한 채 업데이트합니다.

        지정된 필드를 변경하되, 새로운 인스턴스를 생성하여 기존 객체는 그대로 유지합니다.

        Args:
            now (datetime): 업데이트 시각.
            **kwargs: 수정할 필드 값들.

        Returns:
            Self: 수정된 엔터티 인스턴스를 새로 생성하여 반환합니다.
        """
        kwargs.update({"updated_at": now})
        return replace(self, **kwargs)
