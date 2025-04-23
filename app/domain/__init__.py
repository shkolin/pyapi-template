# This is needed for automatic generation of migrations in alembic

from app.domain.admin.admin import Admin  # noqa: F401
from app.domain.base import Base  # noqa: F401
from app.domain.event_log import EventLog  # noqa: F401
from app.domain.user.login import LoginResetRequest  # noqa: F401
from app.domain.user.password import PasswordResetRequest  # noqa: F401
from app.domain.user.user import User  # noqa: F401

__all__: list[str] = []
