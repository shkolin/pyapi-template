from typing import Callable

from faker.proxy import Faker
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.container import AppContainer
from app.domain.user.enum import TokenStatus
from app.domain.user.user import User
from app.mapping.user import UserTable
from app.value_object.user import UserEmail


def test_user_creation(
    session_factory: Callable[..., Session],
    di_container: AppContainer,
    api_client: TestClient,
    faker: Faker,
) -> None:
    email = faker.email()
    plain_password = faker.password()
    request_data = {
        'name': faker.name(),
        'email': email,
        'plain_password': plain_password,
    }
    response = api_client.post('/users', json=request_data)
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}
    with session_factory() as session:
        user: User | None = session.scalars(
            select(User).where(UserTable.c.email == email)
        ).first()
        assert user is not None
        assert user.email == email
        assert (
            di_container.password_hasher().verify(user.password_hash, plain_password)
            is True
        )
        assert user.name == request_data['name']
        session.delete(user)
        session.commit()


def test_reset_password_request(
    session_factory: Callable[..., Session],
    user_factory: Callable[..., User],
    api_client: TestClient,
) -> None:
    with session_factory() as session:
        user = user_factory()
        session.add(user)
        session.commit()
        session.refresh(user)
        assert len(user.password_reset_requests) == 0

        response = api_client.post(
            '/reset-password-request', json={'email': user.email}
        )
        assert response.status_code == 200
        assert response.json() == {'status': 'OK'}

        session.refresh(user)
        assert len(user.password_reset_requests) == 1
        request = user.password_reset_requests[0]

        assert request.expires_at is not None
        assert request.processed_at is None
        assert request.status == TokenStatus.PENDING.value

        session.delete(user)
        session.commit()


def test_recover_password(
    session_factory: Callable[..., Session],
    user_factory: Callable[..., User],
    di_container: AppContainer,
    api_client: TestClient,
) -> None:
    with session_factory() as session:
        user = user_factory()
        request = user.reset_password_request()
        session.add(user)
        session.commit()
        new_plain_password = 'P@$$w0rd'

        response = api_client.post(
            '/recover-password',
            json={'plain_password': new_plain_password, 'token': request.token},
        )
        assert response.status_code == 200
        assert response.json() == {'status': 'OK'}

        session.refresh(user)
        assert (
            di_container.password_hasher().verify(
                user.password_hash, new_plain_password
            )
            is True
        )

        session.refresh(request)
        assert request.expires_at is not None
        assert request.processed_at is not None
        assert request.status == TokenStatus.USED.value

        session.delete(user)
        session.commit()


def test_confirm_email(
    session_factory: Callable[..., Session],
    user_factory: Callable[..., User],
    api_client: TestClient,
    faker: Faker,
) -> None:
    with session_factory() as session:
        old_email = faker.email()
        new_email = faker.email()
        user = user_factory(email=old_email)
        request = user.reset_login_request(UserEmail(new_email))
        session.add(user)
        session.commit()
        session.refresh(user)
        assert user.email_verified is False
        assert len(user.login_reset_requests) == 1
        response = api_client.post('/confirm-email', json={'token': request.token})
        assert response.status_code == 200
        assert response.json() == {'status': 'OK'}
        session.refresh(user)
        assert user.email == new_email
        assert user.email_verified is True
        assert request.expires_at is not None
        assert request.processed_at is not None
        assert request.status == TokenStatus.USED.value
        session.delete(user)
        session.commit()
