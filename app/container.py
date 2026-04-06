from dependency_injector import containers
from dependency_injector import providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.event.manager import EventManager
from app.handler.container import HandlerContainer
from app.service.container import ServiceContainer
from app.uow import UnitOfWork


class AppContainer(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        packages=[
            'app.endpoint',
            'app.domain',
            'app.event',
        ]
    )
    sqlalchemy_engine = providers.Singleton(create_engine, config.db_dsn)
    session_factory = providers.Singleton(
        sessionmaker,
        bind=sqlalchemy_engine,
        expire_on_commit=False,
        autoflush=False,
    )
    unit_of_work = providers.Factory(UnitOfWork, session_factory=session_factory)
    event_manager = providers.Factory(EventManager)
    service = providers.Container(
        ServiceContainer,
        project_name=config.project_name,
        project_url=config.project_url,
        project_email=config.project_email,
        smtp_host=config.smtp_host,
        smtp_port=config.smtp_port,
        smtp_username=config.smtp_username,
        smtp_password=config.smtp_password,
        smtp_use_tls=config.smtp_use_tls,
        jwt_algorithm=config.jwt_algorithm,
        jwt_secret=config.jwt_secret,
        jwt_ttl=config.jwt_ttl,
    )
    handler = providers.Container(
        HandlerContainer,
        service=service,
        event_manager=event_manager,
        unit_of_work=unit_of_work,
    )
