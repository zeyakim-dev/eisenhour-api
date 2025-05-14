from dataclasses import dataclass

from domain.base.entity import Entity


@dataclass(frozen=True, kw_only=True)
class Aggregate(Entity):
    pass
