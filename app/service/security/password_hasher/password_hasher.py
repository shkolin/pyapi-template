from argon2 import PasswordHasher as HashingProvider
from argon2.exceptions import HashingError
from argon2.exceptions import InvalidHashError
from argon2.exceptions import VerificationError
from argon2.exceptions import VerifyMismatchError

from app.service.security.password_hasher.interface import PasswordHasherInterface


class PasswordHasher(PasswordHasherInterface):
    def __init__(self) -> None:
        self.__provider = HashingProvider()

    def hash(self, password: str) -> str:
        try:
            return self.__provider.hash(password)
        except HashingError as e:
            raise ValueError from e

    def verify(self, hash: str, password: str) -> bool:
        try:
            return self.__provider.verify(hash, password)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False
