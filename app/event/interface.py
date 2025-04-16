from abc import ABC
from abc import abstractmethod
from enum import StrEnum
from typing import Any


class EventInterface(StrEnum):
    pass


class EventListenerInterface(ABC):
    @abstractmethod
    def handle(self, event: EventInterface, target: Any, **kwargs: Any) -> None:
        raise NotImplementedError


class EventManagerInterface(ABC):
    @abstractmethod
    def subscribe(self, listener: EventListenerInterface) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, listener: EventListenerInterface) -> None:
        raise NotImplementedError

    @abstractmethod
    def notify(self, event: EventInterface, target: Any, **kwargs: Any) -> None:
        raise NotImplementedError
