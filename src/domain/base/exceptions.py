class TimestampRequiredError(ValueError):
    def __init__(self) -> None:
        super().__init__("created_at and updated_at must be set")
