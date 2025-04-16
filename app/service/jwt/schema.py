from pydantic import BaseModel
from uuid import UUID


class EncodedToken(BaseModel):
    access_token: str
    token_type: str


class DecodedToken(BaseModel):
    sub: UUID
