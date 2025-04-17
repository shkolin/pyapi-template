from pydantic import BaseModel


class AuthorizationViaCredentialsCommand(BaseModel):
    login: str
    plain_password: str


class AuthorizationViaTokenCommand(BaseModel):
    token: str
