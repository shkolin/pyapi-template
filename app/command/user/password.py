from pydantic import BaseModel


class ResetPasswordRequestCommand(BaseModel):
    email: str


class RecoverPasswordCommand(BaseModel):
    plain_password: str
    token: str
