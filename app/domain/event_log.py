from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain import Base


class EventLog(Base):
    __tablename__ = 'events_log'

    id: Mapped[UUID] = mapped_column(postgresql.UUID(as_uuid=True), primary_key=True, index=True)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    admin_id: Mapped[UUID | None] = mapped_column(postgresql.UUID(as_uuid=True), nullable=True)
    entity: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[UUID] = mapped_column(postgresql.UUID(as_uuid=True), nullable=False)
    event: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[dict] = mapped_column(postgresql.JSON, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
