from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

from app.domain.admin.admin import Admin
from app.domain.event_log import EventLog
from app.domain.user.user import User
from app.mapping.base import BaseMetaData

EventLogTable = Table(
    'events_log',
    BaseMetaData,
    Column('id', UUID(True), primary_key=True, index=True),
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True),
    Column('admin_id', ForeignKey('admins.id', ondelete='CASCADE'), nullable=True, index=True),
    Column('entity', String, nullable=False),
    Column('entity_id', UUID(True), nullable=False),
    Column('event', String, nullable=False),
    Column('payload', JSON, nullable=False),
    Column('date_created', DateTime, nullable=False)
)


def perform_mapping() -> None:
    mapper_registry = registry()
    mapper_registry.map_imperatively(
        EventLog,
        EventLogTable,
        properties={
            'user': relationship(User, back_populates='events_log'),
            'admin': relationship(Admin, back_populates='events_log')
        }
    )
