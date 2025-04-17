from dependency_injector import containers
from dependency_injector import providers

from app.repository.container import RepositoryContainer
from app.service.container import ServiceContainer


class AppContainer(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[])
    service = providers.Container(
        ServiceContainer,
        project_name=config.name,
        project_url=config.url,
        project_email=config.email,

        smtp_host=config.smtp.host,
        smtp_port=config.smtp.port,
        smtp_username=config.smtp.username,
        smtp_password=config.smtp.password,
        smtp_use_tls=config.smtp.use_tls,

        jwt_algorithm=config.jwt.algorithm,
        jwt_secret=config.jwt.secret,
        jwt_ttl=config.jwt.ttl
    )
    repository = providers.Container(RepositoryContainer)
