from dependency_injector import containers
from dependency_injector import providers

from app.repository.container import RepositoryContainer
from app.service.container import ServiceContainer


class AppContainer(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[])
    service = providers.Container(ServiceContainer)
    repository = providers.Container(RepositoryContainer)
