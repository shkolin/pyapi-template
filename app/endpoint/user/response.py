from uuid import UUID

from pydantic import BaseModel


class UserDetailsResponse(BaseModel):
    id: UUID
    name: str
    email: str
    email_notify: bool


class FavoriteRaceListItemResponse(BaseModel):
    id: UUID
    title: str
