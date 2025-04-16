from abc import ABC
from abc import abstractmethod
from uuid import UUID

from src.services.jwt.schemas import DecodedToken
from src.services.jwt.schemas import EncodedToken


class JWTServiceInterface(ABC):
    @abstractmethod
    def encode(self, sub: UUID) -> EncodedToken:
        raise NotImplementedError

    @abstractmethod
    def decode(self, token: str) -> DecodedToken:
        raise NotImplementedError
