from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from app.event.interface import EventInterface

if TYPE_CHECKING:
    from app.domain.admin.admin import Admin
    from app.domain.user.user import User


class EventLog:
    def __init__(
        self,
        event: EventInterface,
        entity: str,
        entity_id: UUID,
        payload: dict,
        user: User | None = None,
        admin: Admin | None = None,
    ) -> None:
        self.id = uuid.uuid4()
        self.event = event
        self.entity = entity
        self.entity_id = entity_id
        self.payload = payload
        self.user = user
        self.admin = admin

        self.date_created = datetime.now()
