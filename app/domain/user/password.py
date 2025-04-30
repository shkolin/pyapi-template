from __future__ import annotations

import secrets
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.user.user import User


class PasswordResetRequest:
    def __init__(self, user: User) -> None:
        self.id = uuid.uuid4()
        self.user = user
        self.token = secrets.token_urlsafe(64)
        self.is_used = False
        self.date_requested = datetime.now()
        self.date_used: datetime | None = None

    def verify_token(self) -> None:
        self.date_used = datetime.now()
        self.is_used = True
