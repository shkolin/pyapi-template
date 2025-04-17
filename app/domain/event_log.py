import uuid
from datetime import datetime
from typing import Any
from typing import Optional

from app.domain.user.user import User
from app.event.interface import EventInterface


class EventLog:
    def __init__(
            self,
            user: Optional[User],
            admin: Optional[Any],
            entity: str,
            entity_id: uuid.UUID,
            event: EventInterface,
            payload: dict
    ) -> None:
        self.id = uuid.uuid4()
        self.user = user
        self.admin = admin
        self.entity = entity
        self.entity_id = entity_id
        self.event = event
        self.payload = payload

        self.date_created: datetime = datetime.now()
