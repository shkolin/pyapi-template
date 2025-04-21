from pathlib import Path

from fastapi import FastAPI

from app.container import AppContainer
from app.endpoint.auth.router import router as auth_router
from app.endpoint.exception import AuthorizationError
from app.endpoint.handler import domain_error_handler
from app.endpoint.handler import unauthorized_exception_handler
from app.endpoint.user.router import router as user_router
from app.exception import DomainError

BASE_PATH = Path(__file__).parent.parent.absolute()
ENV_CONFIG = Path(BASE_PATH / 'config.yml')

if not ENV_CONFIG.exists():
    raise RuntimeError('Failed to load configuration file')

container = AppContainer()
container.config.from_yaml(ENV_CONFIG)


def create_app() -> FastAPI:
    api = FastAPI()
    api.include_router(auth_router, tags=['auth'])
    api.include_router(user_router, tags=['users'])

    api.add_exception_handler(AuthorizationError, unauthorized_exception_handler)
    api.add_exception_handler(DomainError, domain_error_handler)

    return api


app = create_app()
