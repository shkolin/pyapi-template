from abc import ABC
from abc import abstractmethod
from uuid import UUID

from app.service.jwt.schema import DecodedToken
from app.service.jwt.schema import EncodedToken


class JWTServiceInterface(ABC):
    @abstractmethod
    def encode(self, sub: UUID) -> EncodedToken:
        raise NotImplementedError

    @abstractmethod
    def decode(self, token: str) -> DecodedToken:
        raise NotImplementedError
