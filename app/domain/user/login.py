import secrets
import uuid
from datetime import datetime

from app.domain.user.user import User


class ResetLoginRequest:
    def __init__(self, user: User, old_login: str, new_login: str) -> None:
        self.id = uuid.uuid4()
        self.user = user
        self.token = secrets.token_urlsafe(64)
        self.old_login = old_login
        self.new_login = new_login
        self.is_used = False
        self.date_requested = datetime.now()
        self.date_used: datetime | None = None

    def verify_token(self) -> None:
        self.date_used = datetime.now()
        self.is_used = True
