from abc import ABC, abstractmethod
from typing import Any


class JWTProvider(ABC):
    """
    JWT 토큰의 생성, 검증, 페이로드 추출을 담당하는 추상 프로바이더.
    """

    @abstractmethod
    def encode(self, payload: dict[str, Any], expires_in: int | None = None) -> str:
        """
        JWT 토큰을 생성합니다.

        Args:
            payload (dict): 토큰에 담을 페이로드
            expires_in (int | None): 만료 시간(초 단위, 옵션)
        Returns:
            str: 생성된 JWT 토큰 문자열
        """
        ...

    @abstractmethod
    def decode(self, token: str) -> dict[str, Any]:
        """
        JWT 토큰을 디코드하여 페이로드를 반환합니다.

        Args:
            token (str): 디코드할 JWT 토큰
        Returns:
            dict: 토큰의 페이로드
        Raises:
            Exception: 토큰이 유효하지 않거나 만료된 경우
        """
        ...

    @abstractmethod
    def is_valid(self, token: str) -> bool:
        """
        JWT 토큰의 유효성을 검사합니다.

        Args:
            token (str): 검사할 JWT 토큰
        Returns:
            bool: 유효하면 True, 아니면 False
        """
        ...
