from abc import ABC, abstractmethod


class Hasher(ABC):
    """비밀번호 해시를 위한 추상 기반 클래스입니다.

    해시 알고리즘 구현체는 이 인터페이스를 구현하여
    비밀번호 저장 및 검증 로직에서 사용됩니다.
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """비밀번호를 해시 문자열로 변환합니다.

        Args:
            password (str): 평문 비밀번호.

        Returns:
            str: 해싱된 비밀번호 문자열.
        """
        pass

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        """주어진 평문 비밀번호와 해시 값을 비교하여 일치 여부를 반환합니다.

        Args:
            password (str): 검증할 평문 비밀번호.
            hashed_password (str): 저장된 해시 비밀번호.

        Returns:
            bool: 비밀번호가 일치하면 True, 그렇지 않으면 False.
        """
        pass
