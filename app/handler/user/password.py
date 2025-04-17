from app.command.user.password import RecoverPasswordCommand
from app.command.user.password import ResetPasswordRequestCommand
from app.exception import DomainError
from app.handler.interface import CommandHandlerInterface
from app.repository.exception import PasswordResetRequestNotFoundError
from app.repository.exception import PersistenceError
from app.repository.exception import UserNotFoundError
from app.repository.user.user import UserRepository
from app.service.mail.user.interface import UserMailServiceInterface
from app.service.smtp.exception import SMTPClientError
from app.uow import UnitOfWorkInterface
from app.value_object.user import UserPassword


class ResetPasswordRequestCommandHandler(CommandHandlerInterface):
    def __init__(
            self,
            uow: UnitOfWorkInterface,
            user_mailer: UserMailServiceInterface
    ) -> None:
        self.__uow = uow
        self.__user_mailer = user_mailer

    def handle(self, command: ResetPasswordRequestCommand) -> None:
        try:
            with self.__uow as uow:
                user = uow.get_repository(UserRepository).get_by_login(command.email)
                request = user.reset_password_request()
            self.__user_mailer.send_password_reset(
                user.email, user.name, request.token
            )
        except (UserNotFoundError, PersistenceError):
            raise DomainError('Failed to reset password request')
        except SMTPClientError:
            raise DomainError('Failed to send notification')


class RecoverPasswordCommandHandler(CommandHandlerInterface):
    def __init__(self, uow: UnitOfWorkInterface) -> None:
        self.__uow = uow

    def handle(self, command: RecoverPasswordCommand) -> None:
        try:
            with self.__uow as uow:
                repo = uow.get_repository(UserRepository)
                request = repo.get_password_reset_request(command.token)
                request.verify_token()
                request.user.update_password(UserPassword(command.plain_password))
        except (PersistenceError, PasswordResetRequestNotFoundError):
            raise DomainError('Failed to recover password')
