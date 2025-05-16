from datetime import datetime, timezone


class TimeProvider:
    """시간 정보를 제공하는 클래스입니다.

    시스템 시간이나 테스트용 시간 생성에 사용됩니다.
    기본적으로 지정된 timezone에 따라 현재 시간을 반환합니다.
    """

    tz: timezone

    def __init__(self, tz: timezone) -> None:
        """TimeProvider를 초기화합니다.

        Args:
            tz (timezone): 반환할 시간에 적용할 타임존.
        """
        self.tz = tz

    def now(self) -> datetime:
        """지정된 타임존 기준의 현재 시간을 반환합니다.

        Returns:
            datetime: 현재 시간.
        """
        return datetime.now(self.tz)
