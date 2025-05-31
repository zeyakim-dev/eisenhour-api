"""
Google 인증 관련 예외 정의.

GoogleSubEmptyError: GoogleSub 값이 비어 있을 때 발생
GoogleSubTooLongError: GoogleSub 값이 너무 길 때 발생
"""


class GoogleSubEmptyError(Exception):
    """
    GoogleSub 값이 비어 있을 때 발생하는 예외.

    Args:
        sub_value (str): 입력된 sub 값
    """

    def __init__(self, sub_value: str) -> None:
        super().__init__(f"GoogleSub 값이 비어 있거나 공백입니다: '{sub_value}'")


class GoogleSubTooLongError(Exception):
    """
    GoogleSub 값이 너무 길 때 발생하는 예외.

    Args:
        sub_value (str): 입력된 sub 값
        max_length (int): 허용 최대 길이
    """

    def __init__(self, sub_value: str, max_length: int) -> None:
        super().__init__(f"GoogleSub 값이 {max_length}자를 초과했습니다: '{sub_value}'")
