class TimestampRequiredError(ValueError):
    """엔터티 생성 시 타임스탬프 누락에 대한 예외입니다.

    `created_at` 또는 `updated_at` 값이 설정되지 않은 경우 발생합니다.
    """

    def __init__(self) -> None:
        """예외 메시지를 설정하여 초기화합니다."""
        super().__init__("created_at and updated_at must be set")
