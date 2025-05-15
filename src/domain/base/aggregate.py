from dataclasses import dataclass

from domain.base.entity import Entity


@dataclass(frozen=True, kw_only=True)
class Aggregate(Entity):
    """도메인 계층의 애그리거트 루트 클래스입니다.

    Entity를 확장하며, 도메인 규칙 상 애그리거트 루트로써 사용됩니다.
    불변성을 유지하며 `id`, `created_at`, `updated_at` 필드를 상속받습니다.
    """

    pass
