from dataclasses import replace
from datetime import datetime
from uuid import uuid4

import pytest

from domain.base.entity import Entity
from domain.base.exceptions import TimestampRequiredError
from shared_kernel.time.time_provider import TimeProvider


class FixedTimeProvider(TimeProvider):
    def __init__(self, dt: datetime):
        self._dt = dt

    def now(self) -> datetime:
        return self._dt


class TestEntity:
    def test_eq_and_hash(self):
        """동일한 UUID를 가진 두 Entity는 동등하며 해시값도 동일해야 한다."""
        dt = datetime(2025, 5, 14, 12, 0, 0)
        custom_id = uuid4()
        e1 = Entity(id=custom_id, created_at=dt, updated_at=dt)
        e2 = Entity(id=custom_id, created_at=dt, updated_at=dt)
        assert e1 == e2
        assert hash(e1) == hash(e2)

    def test_neq_different_type(self):
        """Entity는 다른 타입과 비교할 때 항상 False를 반환해야 한다."""
        dt = datetime.now()
        e = Entity(created_at=dt, updated_at=dt)
        assert not (e == 123)
        assert e != 123

    def test_create_sets_timestamps(self):
        """create()는 현재 시간을 created_at과 updated_at에 설정해야 한다."""
        dt = datetime(2025, 5, 14, 10, 0, 0)
        tp = FixedTimeProvider(dt)
        e = Entity.create(tp)
        assert e.created_at == dt
        assert e.updated_at == dt
        assert hasattr(e, "id") and e.id is not None

    def test_update_updates_updated_at_only(self):
        """update()는 updated_at만 현재 시간으로 갱신해야 한다."""
        dt1 = datetime(2025, 5, 14, 10, 0, 0)
        dt2 = datetime(2025, 5, 14, 11, 0, 0)
        tp1 = FixedTimeProvider(dt1)
        tp2 = FixedTimeProvider(dt2)
        e1 = Entity.create(tp1)
        e2 = e1.update(tp2)

        assert e2.id == e1.id
        assert e2.created_at == e1.created_at
        assert e2.updated_at == dt2
        assert e1.updated_at == dt1

    def test_post_init_raises_on_missing_timestamps(self):
        """created_at 또는 updated_at이 None일 경우 예외를 발생시켜야 한다."""
        with pytest.raises(TimestampRequiredError):
            Entity(created_at=None, updated_at=None)

    def test_hash_in_set(self):
        """동일한 ID를 가진 Entity는 set에서 중복되지 않아야 한다."""
        dt = datetime(2025, 5, 14, 9, 0, 0)
        tp = FixedTimeProvider(dt)
        e1 = Entity.create(tp)
        e2 = replace(e1)
        s = {e1, e2}
        assert len(s) == 1
