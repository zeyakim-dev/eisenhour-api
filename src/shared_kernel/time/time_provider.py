from datetime import datetime, timezone


class TimeProvider:
    tz: timezone

    def __init__(self, tz: timezone) -> None:
        self.tz = tz

    def now(self) -> datetime:
        return datetime.now(self.tz)
