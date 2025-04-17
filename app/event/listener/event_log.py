from typing import Any

from app.event.interface import EventInterface
from app.event.interface import EventListenerInterface
from app.event.listener.event_log_format.format import EventLogFormatFactory


class EventLogListener(EventListenerInterface):
    def __init__(self) -> None:
        self.__formatters = EventLogFormatFactory()

    def handle(self, event: EventInterface, target: Any, **kwargs: Any) -> None:
        pass
