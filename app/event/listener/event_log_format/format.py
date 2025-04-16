from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from app.event.interface import EventInterface

T = TypeVar('T')


class EventLogFormatterError(RuntimeError):
    pass


class EventLogFormatInterface(Generic[T], ABC):
    @abstractmethod
    def format(self, command: T) -> dict:
        raise NotImplementedError


class EventLogFormatFactory:
    __format_map: dict[EventInterface, type[EventLogFormatInterface]] = {
    }

    def get_formatter(self, event: EventInterface) -> EventLogFormatInterface:
        if event not in self.__format_map:
            raise EventLogFormatterError(
                "%s have no configured payload formatters" % event.__class__.__name__
            )

        return self.__format_map[event]()
