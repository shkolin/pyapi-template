import uuid
from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError
from argon2.exceptions import VerifyMismatchError
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from app.domain.user.login import LoginResetRequest
from app.domain.user.password import PasswordResetRequest
from app.value_object.user import UserEmail
from app.value_object.user import UserName
from app.value_object.user import UserPassword


class User:
    def __init__(
            self,
            email: UserEmail,
            plain_password: UserPassword,
            name: UserName,
            email_verified: bool = False
    ) -> None:
        self.id = uuid.uuid4()
        self.email = str(email)
        self.password = self.__hash_password(plain_password)
        self.name = str(name)
        self.last_login_date: datetime | None = None
        self.email_verified = email_verified

        self.date_created = datetime.now()
        self.date_updated: datetime | None = None

        self.reset_password_requests: list[PasswordResetRequest] = []
        self.reset_login_requests: list[LoginResetRequest] = []

    @staticmethod
    @inject
    def __password_hasher(
            password_hasher: PasswordHasher = Provide['password_hasher']
    ) -> PasswordHasher:
        return password_hasher

    def __hash_password(self, plain_password: UserPassword) -> str:
        return self.__password_hasher().hash(str(plain_password))

    def verify_password(self, plain_password: str) -> bool:
        try:
            return self.__password_hasher().verify(self.password, plain_password)
        except (VerifyMismatchError, InvalidHashError):
            return False

    def update_last_login_date(self) -> None:
        self.last_login_date = datetime.now()

    def update_last_modified_date(self) -> None:
        self.date_updated = datetime.now()

    def update_name(self, name: UserName) -> None:
        self.name = str(name)

    def update_password(self, plain_password: UserPassword) -> None:
        self.password = self.__hash_password(plain_password)

    def update_email(self, email: UserEmail) -> None:
        self.email = str(email)

    def confirm_email(self) -> None:
        self.email_verified = True

    def reset_password_request(self) -> PasswordResetRequest:
        request = PasswordResetRequest(self)
        self.reset_password_requests.append(request)
        return request

    def reset_login_request(self, new_login: str) -> LoginResetRequest:
        self.email_verified = False
        request = LoginResetRequest(self, str(self.email), new_login)
        self.reset_login_requests.append(request)
        return request
