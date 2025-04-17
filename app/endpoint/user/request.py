from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str
    plain_password: str


class ResetPasswordRequest(BaseModel):
    email: str


class RecoverPasswordRequest(BaseModel):
    plain_password: str
    token: str
