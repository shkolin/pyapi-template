from pathlib import Path

from fastapi import FastAPI

from app.container import AppContainer

BASE_PATH = Path(__file__).parent.parent.absolute()
ENV_CONFIG = Path(BASE_PATH / 'config.yml')

if not ENV_CONFIG.exists():
    raise RuntimeError('Failed to load configuration file')

container = AppContainer()


def create_app() -> FastAPI:
    container.config.from_yaml(ENV_CONFIG)

    api = FastAPI()

    return api


app = create_app()
