from typing import Callable
from typing import Generator

import pytest
from faker.proxy import Faker
from starlette.testclient import TestClient

from app.domain import User
from app.main import app
from app.main import container
from app.value_object.user import UserEmail
from app.value_object.user import UserName
from app.value_object.user import UserPassword


@pytest.fixture
def di_container() -> Generator:
    yield container


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def user_factory(faker: Faker) -> Callable[..., User]:
    def maker(**kwargs) -> User:
        return User.create(
            UserName(kwargs.get('name', faker.name())),
            UserEmail(kwargs.get('email', faker.email())),
            UserPassword(kwargs.get('plain_password', faker.password()))
        )

    return maker
