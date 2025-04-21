from typing import Callable

import pytest
from sqlalchemy.orm import Session

from app.container import AppContainer
from app.domain import Base


@pytest.fixture(autouse=True)
def initialize_suite(di_container: AppContainer) -> None:
    engine = di_container.sqlalchemy_engine()
    connection = engine.connect()
    transaction = connection.begin()
    for table in Base.metadata.sorted_tables:
        connection.execute(table.delete())
    transaction.commit()


@pytest.fixture
def session_factory(di_container: AppContainer) -> Callable[..., Session]:
    return di_container.scoped_session()
