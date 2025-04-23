from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.domain.base import Base
from app.event.interface import EventInterface

if TYPE_CHECKING:
    from app.domain.user.user import User
    from app.domain.admin.admin import Admin


class EventLog(Base):
    __tablename__ = 'events_log'

    id: Mapped[UUID] = mapped_column(postgresql.UUID(True), primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True
    )
    admin_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('admins.id', ondelete='CASCADE'), nullable=True, index=True
    )
    entity: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[UUID] = mapped_column(postgresql.UUID(True), nullable=False)
    event: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[dict] = mapped_column(postgresql.JSON, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    user: Mapped[Optional['User']] = relationship(
        'User', uselist=False, back_populates='events_log'
    )
    admin: Mapped[Optional['Admin']] = relationship(
        'Admin', uselist=False, back_populates='events_log'
    )

    @classmethod
    def create(
            cls,
            event: EventInterface,
            entity: str,
            entity_id: UUID,
            payload: dict,
            user: Optional['User'],
            admin: Optional['Admin']
    ) -> EventLog:
        obj = cls()
        obj.event = event
        obj.entity = entity
        obj.entity_id = entity_id
        obj.payload = payload
        obj.user = user
        obj.admin = admin
        return obj
