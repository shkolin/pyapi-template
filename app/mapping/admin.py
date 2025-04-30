from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

from app.domain.admin.admin import Admin
from app.domain.event_log import EventLog
from app.mapping.base import BaseMetaData

AdminTable = Table(
    'admins',
    BaseMetaData,
    Column('id', UUID(True), primary_key=True, index=True),
    Column('email', String, nullable=False, unique=True),
    Column('password_hash', String, nullable=False),
    Column('last_login_date', DateTime, nullable=False),
    Column('date_created', DateTime, nullable=False),
    Column('date_updated', DateTime, nullable=True)
)


def perform_mapping() -> None:
    mapper_registry = registry()
    mapper_registry.map_imperatively(
        Admin,
        AdminTable,
        properties={
            'events_log': relationship(
                EventLog,
                uselist=True,
                cascade='all, delete-orphan',
                back_populates='admin'
            )
        }
    )
