from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    email: str
    plain_password: str
    name: str
