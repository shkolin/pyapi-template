from typing import Any

from dependency_injector.wiring import inject

from app.event.interface import EventInterface
from app.event.interface import EventListenerInterface
from app.event.listener.event_log_format.format import EventLogFormatFactory


class EventLogListener(EventListenerInterface):
    @inject
    def __init__(self) -> None:
        self.__formatters = EventLogFormatFactory()

    def handle(self, event: EventInterface, target: Any, **kwargs: Any) -> None:
        payload = {}
        if 'payload' in kwargs:
            payload = self.__formatters.get_formatter(event).format(kwargs['payload'])
