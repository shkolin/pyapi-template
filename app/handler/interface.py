from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

TCommand = TypeVar('TCommand')
TQuery = TypeVar('TQuery')
TResult = TypeVar('TResult')


class QueryHandlerInterface(ABC, Generic[TQuery, TResult]):
    @abstractmethod
    def handle(self, query: TQuery) -> TResult:
        raise NotImplementedError


class CommandHandlerInterface(ABC, Generic[TCommand, TResult]):
    @abstractmethod
    def handle(self, command: TCommand) -> TResult:
        raise NotImplementedError
