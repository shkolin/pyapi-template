from typing import Callable

from faker.proxy import Faker
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.container import AppContainer
from app.domain.user.user import User


def test_user_creation(
        session_factory: Callable[..., Session],
        di_container: AppContainer,
        api_client: TestClient,
        faker: Faker
) -> None:
    email = faker.email()
    plain_password = faker.password()
    request_data = {
        'name': faker.name(),
        'email': email,
        'plain_password': plain_password
    }
    response = api_client.post('/users', json=request_data)
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}
    with session_factory() as session:
        user: User | None = session.scalars(
            select(User).where(User.email == email)
        ).first()
        assert user is not None
        assert user.email == email
        assert di_container.password_hasher().verify(user.password_hash, plain_password) is True
        assert user.name == request_data['name']
        session.delete(user)
        session.commit()
