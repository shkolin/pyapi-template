import copy
from typing import Any

from app.event.interface import EventInterface
from app.event.interface import EventListenerInterface
from app.event.interface import EventManagerInterface


class EventManager(EventManagerInterface):
    def __init__(self) -> None:
        self.__listeners: set[EventListenerInterface] = set()

    @property
    def listeners(self) -> set[EventListenerInterface]:
        return copy.copy(self.__listeners)

    def subscribe(self, listener: EventListenerInterface) -> None:
        if listener not in self.__listeners:
            self.__listeners.add(listener)

    def unsubscribe(self, listener: EventListenerInterface) -> None:
        if listener in self.__listeners:
            self.__listeners.remove(listener)

    def notify(self, event: EventInterface, target: Any, **kwargs: Any) -> None:
        for listener in self.__listeners:
            listener.handle(event, target, **kwargs)
