from datetime import timedelta
from typing import Any

import jwt

from application.ports.jwt_provider.jwt_provider import JWTProvider
from shared_kernel.time.time_provider import TimeProvider


class PyJWTProvider(JWTProvider):
    """
    PyJWT 기반 JWTProvider 실제 구현체.
    """

    def __init__(
        self, time_provider: TimeProvider, secret: str, algorithm: str = "HS256"
    ):
        self.time_provider = time_provider
        self.secret = secret
        self.algorithm = algorithm

    def encode(self, payload: dict[str, Any], expires_in: int | None = None) -> str:
        to_encode = payload.copy()
        if expires_in is not None:
            expire = self.time_provider.now() + timedelta(seconds=expires_in)
            to_encode["exp"] = expire
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def decode(self, token: str) -> Any:
        return jwt.decode(
            token,
            self.secret,
            algorithms=[self.algorithm],
            options={"verify_exp": True},
        )

    def is_valid(self, token: str) -> bool:
        try:
            jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                options={"verify_exp": True},
            )
        except jwt.PyJWTError:
            return False
        return True
