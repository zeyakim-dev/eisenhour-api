from dataclasses import dataclass

from domain.base.entity import Entity


@dataclass(frozen=True, kw_only=True)
class Aggregate(Entity):
    """도메인 계층의 애그리거트 루트 클래스입니다.

    도메인 모델에서 애그리거트 루트로 사용되는 불변 엔터티입니다.
    상위 Entity 클래스로부터 고유 식별자 및 타임스탬프 필드를 상속받습니다.

    불변성과 ID 기반 동등성 비교를 유지하며,
    도메인 규칙상 트랜잭션 경계를 책임지는 루트 엔터티로 작동합니다.
    """

    pass
