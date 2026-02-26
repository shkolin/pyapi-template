import uuid
from datetime import datetime

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from sqlalchemy.orm import reconstructor

from app.domain.event_log import EventLog
from app.domain.user.enum import UserStatus
from app.domain.user.login import LoginResetRequest
from app.domain.user.password import PasswordResetRequest
from app.service.security.password_hasher.interface import PasswordHasherInterface
from app.value_object.user import UserEmail
from app.value_object.user import UserName
from app.value_object.user import UserPassword


class User:
    def __init__(
        self,
        name: UserName,
        email: UserEmail,
        plain_password: UserPassword,
        password_hasher: PasswordHasherInterface,
        status: UserStatus = UserStatus.ACTIVE,
    ) -> None:
        self.id = uuid.uuid4()
        self.email = str(email)
        self.name = str(name)
        self.last_login_date: datetime | None = None
        self.email_verified = False
        self.status = status.value

        self.created_at: datetime = datetime.now()
        self.updated_at: datetime | None = None

        self.password_reset_requests: list[PasswordResetRequest] = []
        self.login_reset_requests: list[LoginResetRequest] = []
        self.events_log: list[EventLog] = []

        self.password_hash = password_hasher.hash(str(plain_password))
        self.__password_hasher = password_hasher

    @inject
    @reconstructor
    def __orm_init__(
        self,
        hasher: PasswordHasherInterface = Provide['service.password_hasher'],
    ) -> None:
        self.__password_hasher = hasher

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE.value

    def verify_password(self, plain_password: str) -> bool:
        return self.__password_hasher.verify(self.password_hash, plain_password)

    def update_last_login_date(self) -> None:
        self.last_login_date = datetime.now()

    def update_last_modified_date(self) -> None:
        self.updated_at = datetime.now()

    def update_password(self, plain_password: UserPassword) -> None:
        self.password_hash = self.__password_hasher.hash(str(plain_password))

    def update_email(self, email: UserEmail) -> None:
        self.email = str(email)

    def confirm_email(self) -> None:
        self.email_verified = True

    def reset_password_request(self) -> PasswordResetRequest:
        request = PasswordResetRequest(self)
        self.password_reset_requests.append(request)
        return request

    def reset_login_request(self, new_login: UserEmail) -> LoginResetRequest:
        self.email_verified = False
        request = LoginResetRequest(self, new_login)
        self.login_reset_requests.append(request)
        return request
