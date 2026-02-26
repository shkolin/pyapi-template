from abc import ABC
from abc import abstractmethod


class PasswordHasherInterface(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, hash: str, password: str) -> bool:
        raise NotImplementedError
