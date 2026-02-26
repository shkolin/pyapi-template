from typing import Callable

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.container import AppContainer
from app.domain.user.user import User
from app.service.jwt.interface import JWTServiceInterface
from app.service.jwt.schema import DecodedToken


def test_authorization_via_credentials(
    session_factory: Callable[..., Session],
    user_factory: Callable[..., User],
    di_container: AppContainer,
    api_client: TestClient,
) -> None:
    with session_factory() as session:
        plain_password = 'P@$$w0rd'
        user = user_factory(plain_password=plain_password)
        user.confirm_email()
        session.add(user)
        session.commit()
        response = api_client.post(
            '/auth',
            data={
                'username': user.email,
                'password': plain_password,
            },
        )
        assert response.status_code == 200
        json = response.json()
        assert json['token_type'] == 'bearer'
        jwt: JWTServiceInterface = di_container.service.jwt()
        data: DecodedToken = jwt.decode(json['access_token'])
        assert user.id == data.sub
        session.delete(user)
        session.commit()
