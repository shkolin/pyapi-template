from dependency_injector import containers
from dependency_injector import providers
from sqlalchemy.orm import Session

from app.repository.user.user import UserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    session = providers.Dependency(instance_of=Session)
    user = providers.Factory(UserRepository, session=session)
