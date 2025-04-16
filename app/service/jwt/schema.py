from uuid import UUID

from pydantic import BaseModel


class EncodedToken(BaseModel):
    access_token: str
    token_type: str


class DecodedToken(BaseModel):
    sub: UUID
