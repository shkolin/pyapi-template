from typing import Generator

from argon2 import PasswordHasher
from dependency_injector import containers
from dependency_injector import providers
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from app.event.manager import EventManager
from app.handler.container import HandlerContainer
from app.repository.container import RepositoryContainer
from app.service.container import ServiceContainer
from app.uow import UnitOfWork


def init_database_session(session_init_factory: scoped_session) -> Generator:
    session = session_init_factory()
    yield session
    session_init_factory.remove()


class AppContainer(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()
    wiring_config = containers.WiringConfiguration(packages=[
        'app.endpoint',
        'app.domain',
        'app.event'
    ])
    sqlalchemy_engine = providers.Singleton(create_engine, config.db.dsn)
    session_factory = providers.Singleton(
        sessionmaker,
        bind=sqlalchemy_engine,
        expire_on_commit=False,
        autoflush=False
    )
    scoped_session = providers.Factory(scoped_session, session_factory)
    session = providers.Resource(
        init_database_session, session_init_factory=scoped_session
    )
    unit_of_work = providers.Factory(UnitOfWork, session=session)
    event_manager = providers.Factory(EventManager)
    password_hasher = providers.Factory(PasswordHasher)
    service = providers.Container(
        ServiceContainer,
        project_name=config.project.name,
        project_url=config.project.url,
        project_email=config.project.email,

        smtp_host=config.smtp.host,
        smtp_port=config.smtp.port,
        smtp_username=config.smtp.username,
        smtp_password=config.smtp.password,
        smtp_use_tls=config.smtp.use_tls,

        jwt_algorithm=config.jwt.algorithm,
        jwt_secret=config.jwt.secret,
        jwt_ttl=config.jwt.ttl
    )
    repository = providers.Container(RepositoryContainer, session=session)
    handler = providers.Container(
        HandlerContainer,
        repository=repository,
        service=service,
        event_manager=event_manager,
        unit_of_work=unit_of_work
    )
