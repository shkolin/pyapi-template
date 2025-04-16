from abc import ABC
from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar('ModelType', bound=object)


class BaseRepository(ABC, Generic[ModelType]):
    def __init__(self, session: Session):
        self._session = session

    def add(self, obj: ModelType) -> None:
        self._session.add(obj)

    def delete(self, obj: ModelType) -> None:
        self._session.delete(obj)
