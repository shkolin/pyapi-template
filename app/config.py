from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = ''
    project_email: str = ''
    project_url: str = ''

    db_dsn: str = 'postgresql+psycopg2://user:password@localhost/db'

    smtp_host: str = 'localhost'
    smtp_port: int = 1025
    smtp_username: str = ''
    smtp_password: str = ''
    smtp_use_tls: bool = False

    jwt_algorithm: str = 'HS256'
    jwt_secret: str = ''
    jwt_ttl: int = 86400

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.absolute() / '.env',
    )


__all__ = ['Settings']
