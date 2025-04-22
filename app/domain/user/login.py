from __future__ import annotations

import secrets
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import false
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.domain.base import Base
from app.value_object.user import UserEmail

if TYPE_CHECKING:
    from app.domain.user.user import User


class LoginResetRequest(Base):
    __tablename__ = 'login_reset_requests'

    id: Mapped[UUID] = mapped_column(postgresql.UUID(True), primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)
    old_login: Mapped[str] = mapped_column(String, nullable=False)
    new_login: Mapped[str] = mapped_column(String, nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    date_requested: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    date_used: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped['User'] = relationship(
        'User', back_populates='login_reset_requests'
    )

    @classmethod
    def create(
            cls,
            user: User,
            old_login: UserEmail,
            new_login: UserEmail
    ) -> LoginResetRequest:
        request = cls()
        request.user = user
        request.token = secrets.token_urlsafe(64)
        request.old_login = str(old_login)
        request.new_login = str(new_login)
        return request

    def verify_token(self) -> None:
        self.date_used = datetime.now()
        self.is_used = True
