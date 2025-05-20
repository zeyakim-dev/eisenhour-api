import bcrypt

from shared_kernel.hasher.hasher import Hasher


class BcryptHasher(Hasher):
    """Bcrypt 알고리즘을 사용하는 비밀번호 해시 구현체입니다."""

    def hash(self, password: str) -> str:
        """비밀번호를 bcrypt로 해시합니다.

        Args:
            password (str): 평문 비밀번호.

        Returns:
            str: 해시된 비밀번호 문자열.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    def verify(self, password: str, hashed_password: str) -> bool:
        """bcrypt로 해시된 비밀번호와 평문 비밀번호를 비교합니다.

        Args:
            password (str): 검증할 평문 비밀번호.
            hashed_password (str): 저장된 해시 비밀번호.

        Returns:
            bool: 비밀번호가 일치하면 True, 그렇지 않으면 False.
        """
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
