from __future__ import annotations

import uuid
from datetime import datetime
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError
from argon2.exceptions import VerifyMismatchError
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import false
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.domain.base import Base
from app.domain.event_log import EventLog
from app.domain.user.login import LoginResetRequest
from app.domain.user.password import PasswordResetRequest
from app.value_object.user import UserEmail
from app.value_object.user import UserName
from app.value_object.user import UserPassword


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(postgresql.UUID(True), primary_key=True, index=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    last_login_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    date_created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    date_updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    password_reset_requests: Mapped[list['PasswordResetRequest']] = relationship(
        'PasswordResetRequest', uselist=True, cascade='all, delete-orphan', back_populates='user'
    )
    login_reset_requests: Mapped[list['LoginResetRequest']] = relationship(
        'LoginResetRequest', uselist=True, cascade='all, delete-orphan', back_populates='user'
    )
    events_log: Mapped[list['EventLog']] = relationship(
        'EventLog', uselist=True, cascade='all, delete-orphan', back_populates='user'
    )

    @classmethod
    def create(
            cls,
            name: UserName,
            email: UserEmail,
            plain_password: UserPassword
    ) -> User:
        obj = cls()
        obj.name = str(name)
        obj.email = str(email)
        obj.password_hash = cls.__password_hasher().hash(str(plain_password))
        return obj

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

    def update_last_login_date(self) -> None:
        self.last_login_date = datetime.now()

    def update_last_modified_date(self) -> None:
        self.date_updated = datetime.now()

    def update_password(self, plain_password: UserPassword) -> None:
        self.password_hash = self.__password_hasher().hash(str(plain_password))

    def update_email(self, email: UserEmail) -> None:
        self.email = str(email)

    def confirm_email(self) -> None:
        self.email_verified = True

    def reset_password_request(self) -> PasswordResetRequest:
        request = PasswordResetRequest.create(self)
        self.password_reset_requests.append(request)
        return request

    def reset_login_request(self, new_login: UserEmail) -> LoginResetRequest:
        self.email_verified = False
        request = LoginResetRequest.create(self, UserEmail(self.email), new_login)
        self.login_reset_requests.append(request)
        return request
