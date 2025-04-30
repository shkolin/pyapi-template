import uuid
from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError
from argon2.exceptions import VerifyMismatchError
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from app.domain.event_log import EventLog


class Admin:
    def __init__(self, email: str, plain_password: str) -> None:
        self.id = uuid.uuid4()
        self.email = email
        self.password_hash = self.__password_hasher().hash(plain_password)
        self.last_login_date: datetime | None = None

        self.date_created = datetime.now()
        self.date_updated: datetime | None = None

        self.events_log: list[EventLog] = []

    @staticmethod
    @inject
    def __password_hasher(
            password_hasher: PasswordHasher = Provide['password_hasher']
    ) -> PasswordHasher:
        return password_hasher

    def verify_password(self, plain_password: str) -> bool:
        try:
            return self.__password_hasher().verify(self.password_hash, plain_password)
        except (VerifyMismatchError, InvalidHashError):
            return False
