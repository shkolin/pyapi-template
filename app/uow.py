from abc import ABC
from abc import abstractmethod
from types import TracebackType
from typing import Optional
from typing import Self
from typing import Type
from typing import TypeVar
from typing import cast

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.repository.base import BaseRepository
from app.repository.exception import PersistenceError

RepoType = TypeVar('RepoType', bound=BaseRepository)


class UnitOfWorkInterface(ABC):
    @abstractmethod
    def get_repository(self, repo_class: Type[RepoType]) -> RepoType:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
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
    def __init__(self, session_factory: sessionmaker):
        self.__session_factory = session_factory
        self.__session: Session | None = None
        self.__repo_cache: dict[type[BaseRepository], BaseRepository] = {}
        self.__entered = False

    def __enter__(self) -> Self:
        self.begin()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        except SQLAlchemyError as e:
            raise PersistenceError(str(e))
        finally:
            self.close()

    def begin(self) -> None:
        if not self.__entered:
            self.__entered = True
            self.__session = self.__session_factory()

    def commit(self) -> None:
        assert self.__session is not None
        self.__session.commit()

    def rollback(self) -> None:
        assert self.__session is not None
        self.__session.rollback()

    def close(self) -> None:
        self.__repo_cache.clear()
        self.__entered = False
        if self.__session is not None:
            self.__session.close()
            self.__session = None

    def get_repository(self, repo_class: Type[RepoType]) -> RepoType:
        if repo_class not in self.__repo_cache:
            if not self.__session:
                raise RuntimeError(
                    'No active transaction. Did you forget to call begin()?'
                )
            self.__repo_cache[repo_class] = repo_class(self.__session)
        return cast(RepoType, self.__repo_cache[repo_class])
