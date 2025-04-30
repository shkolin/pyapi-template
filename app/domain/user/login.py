from __future__ import annotations

import secrets
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

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
        self.is_used = False
        self.date_requested = datetime.now()
        self.date_used: datetime | None = None

    def verify_token(self) -> None:
        self.date_used = datetime.now()
        self.is_used = True
