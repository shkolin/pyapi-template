from pydantic import BaseModel

from src.command.base import BaseCommand
from src.domain.user import User


class ResetPasswordRequestCommand(BaseModel):
    email: str


class RecoverPasswordCommand(BaseModel):
    plain_password: str
    token: str
