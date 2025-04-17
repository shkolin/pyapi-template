from app.command.user.email import ConfirmEmailCommand
from app.exception import DomainError
from app.handler.interface import CommandHandlerInterface
from app.repository.exception import LoginResetRequestNotFoundError
from app.repository.user.user import UserRepository
from app.service.mail.user.interface import UserMailServiceInterface
from app.uow import UnitOfWorkInterface
from app.value_object.user import UserEmail


class ConfirmEmailCommandHandler(CommandHandlerInterface):
    def __init__(
            self,
            uow: UnitOfWorkInterface,
            user_mailer: UserMailServiceInterface
    ) -> None:
        self.__uow = uow
        self.__user_mailer = user_mailer

    def handle(self, command: ConfirmEmailCommand) -> None:
        try:
            with self.__uow as uow:
                repo = uow.get_repository(UserRepository)
                request = repo.get_login_reset_request(command.token)
                request.verify_token()
                request.user.update_email(UserEmail(request.new_login))
                request.user.confirm_email()
            self.__user_mailer.send_welcome(request.user.email, request.user.name)
        except LoginResetRequestNotFoundError:
            raise DomainError('Failed to confirm email address')
