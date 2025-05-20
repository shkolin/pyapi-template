from dependency_injector import containers
from dependency_injector import providers

from app.event.manager import EventManager
from app.handler.auth import AuthorizationViaCredentialsCommandHandler
from app.handler.auth import AuthorizationViaTokenCommandHandler
from app.handler.command.user.create_user import CreateUserCommandHandler
from app.handler.command.user.email import ConfirmEmailCommandHandler
from app.handler.command.user.password import RecoverPasswordCommandHandler
from app.handler.command.user.password import ResetPasswordRequestCommandHandler
from app.uow import UnitOfWork


class HandlerContainer(containers.DeclarativeContainer):
    service = providers.DependenciesContainer()
    repository = providers.DependenciesContainer()
    event_manager = providers.Dependency(instance_of=EventManager)
    unit_of_work = providers.Dependency(instance_of=UnitOfWork)

    create_user = providers.Factory(
        CreateUserCommandHandler,
        user_mailer=service.user_mailer,
        event_manager=event_manager,
        uow=unit_of_work,
    )
    authorization_via_credentials = providers.Factory(
        AuthorizationViaCredentialsCommandHandler, uow=unit_of_work, jwt=service.jwt
    )
    authorization_via_token = providers.Factory(
        AuthorizationViaTokenCommandHandler, uow=unit_of_work, jwt=service.jwt
    )
    reset_password_request = providers.Factory(
        ResetPasswordRequestCommandHandler,
        uow=unit_of_work,
        user_mailer=service.user_mailer,
        event_manager=event_manager,
    )
    recover_password = providers.Factory(
        RecoverPasswordCommandHandler, uow=unit_of_work
    )
    confirm_email = providers.Factory(
        ConfirmEmailCommandHandler, uow=unit_of_work, user_mailer=service.user_mailer
    )
