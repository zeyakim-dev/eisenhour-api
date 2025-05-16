class TimestampRequiredError(ValueError):
    """엔터티 생성 시 필수 타임스탬프 누락에 대한 예외입니다.

    `created_at` 또는 `updated_at` 필드가 None인 경우 발생하며,
    도메인 엔터티의 유효성 확보를 위한 방어적 예외입니다.
    """

    def __init__(self) -> None:
        """예외 메시지를 설정하여 초기화합니다."""
        super().__init__("created_at and updated_at must be set")
