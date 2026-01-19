from __future__ import annotations

import secrets
import uuid
from datetime import datetime
from datetime import timedelta
from typing import TYPE_CHECKING

from app.domain.user.enum import TokenStatus
from app.value_object.user import UserEmail

if TYPE_CHECKING:
    from app.domain.user.user import User


class LoginResetRequest:
    def __init__(self, user: User, new_login: UserEmail) -> None:
        self.id = uuid.uuid4()
        self.user = user
        self.token = secrets.token_urlsafe(64)
        self.old_login = user.email
        self.new_login = str(new_login)
        self.status = TokenStatus.PENDING.value
        self.requested_at = datetime.now()
        self.processed_at: datetime | None = None
        self.expires_at = datetime.now() + timedelta(hours=1)

    def verify_token(self) -> None:
        self.status = TokenStatus.USED.value
        self.processed_at = datetime.now()
