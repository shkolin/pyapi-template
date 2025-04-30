from typing import Any

from dependency_injector.wiring import Provide

from app.domain.event_log import EventLog
from app.domain.user.user import User
from app.event.interface import EventInterface
from app.event.interface import EventListenerInterface
from app.event.listener.event_log_format.format import EventLogFormatFactory
from app.repository.event_log.event_log import EventLogRepository
from app.uow import UnitOfWorkInterface


class EventLogListener(EventListenerInterface):
    def __init__(self, uow: UnitOfWorkInterface = Provide['unit_of_work']) -> None:
        self.__uow = uow
        self.__formatters = EventLogFormatFactory()

    def handle(self, event: EventInterface, target: Any, **kwargs: Any) -> None:
        user: User | None = None
        admin = None
        if 'user' in kwargs:
            user = kwargs['user']

        payload = {}
        if 'payload' in kwargs:
            payload = self.__formatters.get_formatter(event).format(kwargs['payload'])

        event_log = EventLog(
            event, target.__class__.__name__, target.id, payload, user, admin
        )

        with self.__uow as uow:
            uow.get_repository(EventLogRepository).add(event_log)
