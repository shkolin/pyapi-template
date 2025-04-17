from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import false
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

from app.domain.user.login import LoginResetRequest
from app.domain.user.password import PasswordResetRequest
from app.domain.user.user import User
from app.mapping.base import BaseMetaData

UserTable = Table(
    'users',
    BaseMetaData,
    Column('id', UUID(True), primary_key=True, index=True),
    Column('email', String, unique=True, nullable=False),
    Column('password', String, nullable=False),
    Column('name', String, nullable=False),
    Column('last_login_date', DateTime, nullable=True),
    Column('email_notify', Boolean, nullable=False, server_default=false()),
    Column('email_verified', Boolean, nullable=False, server_default=false()),
    Column('auth_provider', String, nullable=True),
    Column('auth_provider_id', String, nullable=True),
    Column('date_created', DateTime, nullable=False),
    Column('date_updated', DateTime)
)

LoginResetRequestTable = Table(
    'login_reset_requests',
    BaseMetaData,
    Column('id', UUID(True), primary_key=True, index=True),
    Column(
        'user_id',
        ForeignKey(UserTable.c.id, ondelete='CASCADE'),
        nullable=False,
        index=True,
    ),
    Column('token', String, nullable=False),
    Column('old_email', String, nullable=False),
    Column('new_email', String, nullable=False),
    Column('is_used', Boolean, nullable=False, server_default=false()),
    Column('date_requested', DateTime, nullable=False),
    Column('date_used', DateTime, nullable=True)
)

PasswordResetRequestTable = Table(
    'password_reset_requests',
    BaseMetaData,
    Column('id', UUID(True), primary_key=True, index=True),
    Column(
        'user_id',
        ForeignKey(UserTable.c.id, ondelete='CASCADE'),
        nullable=False,
        index=True,
    ),
    Column('token', String, nullable=False, index=True),
    Column('is_used', Boolean, nullable=False, server_default=false()),
    Column('date_requested', DateTime, nullable=False),
    Column('date_used', DateTime, nullable=True)
)


def perform_mapping() -> None:
    mapper_registry = registry()
    mapper_registry.map_imperatively(
        User,
        UserTable,
        properties={
            'password_reset_requests': relationship(
                PasswordResetRequest,
                cascade='all, delete-orphan',
                uselist=True,
                back_populates='user',
                lazy='joined'
            ),
            'login_reset_requests': relationship(
                LoginResetRequest,
                cascade='all, delete-orphan',
                uselist=True,
                back_populates='user',
                lazy='joined'
            )
        }
    )
    mapper_registry.map_imperatively(
        PasswordResetRequest,
        PasswordResetRequestTable,
        properties={
            'user': relationship(User, back_populates='password_reset_requests')
        }
    )
    mapper_registry.map_imperatively(
        LoginResetRequest,
        LoginResetRequestTable,
        properties={
            'user': relationship(User, back_populates='login_reset_requests')
        }
    )
