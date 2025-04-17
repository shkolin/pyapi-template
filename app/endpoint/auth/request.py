from pydantic import BaseModel


class AuthorizationRequest(BaseModel):
    login: str
    plain_password: str
