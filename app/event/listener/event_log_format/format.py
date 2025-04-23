from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from app.command.user.create_user import CreateUserCommand
from app.command.user.password import ResetPasswordRequestCommand
from app.event.event import UserEvent
from app.event.interface import EventInterface

T = TypeVar('T')


class EventLogFormatterError(RuntimeError):
    pass


class EventLogFormatInterface(Generic[T], ABC):
    @abstractmethod
    def format(self, command: T) -> dict:
        raise NotImplementedError


class UserRegistrationFormatter(EventLogFormatInterface[CreateUserCommand]):
    def format(self, command: CreateUserCommand) -> dict:
        return {
            'email': command.email,
            'name': command.name
        }


class UserResetLoginRequestFormatter(EventLogFormatInterface[ResetPasswordRequestCommand]):
    def format(self, command: ResetPasswordRequestCommand) -> dict:
        return {
            'email': command.email
        }


class EventLogFormatFactory:
    __format_map: dict[EventInterface, type[EventLogFormatInterface]] = {
        UserEvent.REGISTERED: UserRegistrationFormatter,
        UserEvent.RESET_PASSWORD_REQUESTED: UserResetLoginRequestFormatter
    }

    def get_formatter(self, event: EventInterface) -> EventLogFormatInterface:
        if event not in self.__format_map:
            raise EventLogFormatterError(
                "%s have no configured payload formatters" % event.__class__.__name__
            )

        return self.__format_map[event]()
