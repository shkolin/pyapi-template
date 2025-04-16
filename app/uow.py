from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from types import TracebackType
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import cast

from sqlalchemy.orm import Session

from app.repository.base import BaseRepository

RepoType = TypeVar('RepoType', bound=BaseRepository)


class UnitOfWorkInterface(ABC):
    @abstractmethod
    def get_repository(self, repo_class: Type[RepoType]) -> RepoType:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> UnitOfWorkInterface:
        raise NotImplementedError

    @abstractmethod
    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> bool | None:
        raise NotImplementedError

    @abstractmethod
    def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class UnitOfWork(UnitOfWorkInterface):
    def __init__(self, session: Session):
        self.__session = session
        self.__repo_cache: dict[type[BaseRepository], BaseRepository] = {}
        self.__entered = False

    def __enter__(self) -> UnitOfWork:
        self.begin()
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> bool | None:
        try:
            if exc_type:
                self.rollback()
                return False
            else:
                self.commit()
        finally:
            self.close()
        return None

    def begin(self) -> None:
        if not self.__entered:
            self.__entered = True
            if not self.__session.in_transaction():
                self.__session.begin()

    def commit(self) -> None:
        if not self.__session.in_transaction():
            raise RuntimeError('No active transaction. Did you forget to call begin()?')
        self.__session.commit()

    def rollback(self) -> None:
        if self.__session.in_transaction():
            self.__session.rollback()

    def close(self) -> None:
        self.__repo_cache.clear()
        self.__entered = False

    def get_repository(self, repo_class: Type[RepoType]) -> RepoType:
        if repo_class not in self.__repo_cache:
            self.__repo_cache[repo_class] = repo_class(self.__session)
        return cast(RepoType, self.__repo_cache[repo_class])
