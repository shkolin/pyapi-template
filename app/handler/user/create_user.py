from app.command.user.create_user import CreateUserCommand
from app.domain.user.user import User
from app.event.event import UserEvent
from app.event.interface import EventManagerInterface
from app.event.listener.event_log import EventLogListener
from app.exception import DomainError
from app.handler.interface import CommandHandlerInterface
from app.repository.exception import PersistenceError
from app.repository.user.user import UserRepository
from app.service.mail.user.interface import UserMailServiceInterface
from app.service.smtp.exception import SMTPClientError
from app.uow import UnitOfWorkInterface
from app.value_object.user import UserEmail
from app.value_object.user import UserName
from app.value_object.user import UserPassword


class CreateUserCommandHandler(CommandHandlerInterface):
    def __init__(
            self,
            user_mailer: UserMailServiceInterface,
            event_manager: EventManagerInterface,
            uow: UnitOfWorkInterface
    ) -> None:
        self.__event_manager = event_manager
        self.__user_mailer = user_mailer
        self.__uow = uow

        self.__event_manager.subscribe(EventLogListener())

    def handle(self, command: CreateUserCommand) -> None:
        try:
            with self.__uow as uow:
                email = UserEmail(command.email)
                user = User.create(UserName(command.name), email, UserPassword(command.plain_password))
                login_reset = user.reset_login_request(email)
                uow.get_repository(UserRepository).add(user)

            self.__event_manager.notify(
                UserEvent.REGISTERED, user, payload=command, user=user
            )
            self.__user_mailer.send_email_confirmation(
                user.email, user.name, login_reset.token
            )
        except PersistenceError:
            raise DomainError('Failed to create user')
        except SMTPClientError:
            raise DomainError('Failed to send notification')
