from __future__ import annotations

import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.domain.base import Base
from app.domain.event_log import EventLog


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[UUID] = mapped_column(postgresql.UUID(True), primary_key=True, index=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    last_login_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    date_updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    events_log: Mapped[list['EventLog']] = relationship(
        'EventLog', uselist=True, cascade='all, delete-orphan', back_populates='admin'
    )
