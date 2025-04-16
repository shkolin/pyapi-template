from datetime import datetime
from datetime import timedelta
from datetime import timezone
from uuid import UUID

import jwt

from app.service.jwt.exception import JWTServiceError
from app.service.jwt.interface import JWTServiceInterface
from app.service.jwt.schema import DecodedToken
from app.service.jwt.schema import EncodedToken


class JWTService(JWTServiceInterface):
    def __init__(self, algorithms: str, secret: str, ttl: int) -> None:
        self.__algorithms = algorithms
        self.__secret = secret
        self.__ttl = ttl

    def encode(self, sub: UUID) -> EncodedToken:
        return EncodedToken(
            access_token=jwt.encode(
                {
                    'exp': datetime.now(tz=timezone.utc)
                           + timedelta(seconds=self.__ttl),
                    'sub': str(sub),
                },
                self.__secret,
                self.__algorithms,
            ),
            token_type='bearer',
        )

    def decode(self, token: str) -> DecodedToken:
        try:
            data = jwt.decode(token, self.__secret, algorithms=[self.__algorithms])
            return DecodedToken(sub=UUID(data['sub']))
        except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
            raise JWTServiceError(e)
