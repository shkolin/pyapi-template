from dependency_injector import containers
from dependency_injector import providers


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
