from app.command.auth import AuthorizationViaCredentialsCommand
from app.command.auth import AuthorizationViaTokenCommand
from app.domain.user.user import User
from app.endpoint.auth.response import Token
from app.endpoint.exception import AuthorizationError
from app.exception import DomainError
from app.handler.interface import CommandHandlerInterface
from app.repository.exception import PersistenceError
from app.repository.user.exception import UserNotFoundError
from app.repository.user.user import UserRepository
from app.service.jwt.exception import JWTServiceError
from app.service.jwt.interface import JWTServiceInterface
from app.uow import UnitOfWorkInterface


class AuthorizationViaCredentialsCommandHandler(CommandHandlerInterface):
    def __init__(
            self,
            uow: UnitOfWorkInterface,
            jwt: JWTServiceInterface
    ) -> None:
        self.__uow = uow
        self.__jwt = jwt

    def handle(self, command: AuthorizationViaCredentialsCommand) -> Token:
        try:
            with self.__uow as uow:
                user = uow.get_repository(UserRepository).get_by_login(command.login)
                if not user.verify_password(command.plain_password):
                    raise AuthorizationError('Invalid login or password')
                if not user.email_verified:
                    raise AuthorizationError('Email not verified')
                user.update_last_login_date()
        except (UserNotFoundError,
                AuthorizationError,
                PersistenceError):
            raise DomainError('Failed to authorization')

        return Token(**self.__jwt.encode(user.id).model_dump())


class AuthorizationViaTokenCommandHandler(CommandHandlerInterface):
    def __init__(
            self,
            uow: UnitOfWorkInterface,
            jwt: JWTServiceInterface
    ) -> None:
        self.__uow = uow
        self.__jwt = jwt

    def handle(self, command: AuthorizationViaTokenCommand) -> User:
        try:
            with self.__uow as uow:
                data = self.__jwt.decode(command.token)
                user = uow.get_repository(UserRepository).get_by_id(data.sub)
                if not user.email_verified:
                    raise AuthorizationError('Email not verified')
                user.update_last_login_date()
            return user
        except (JWTServiceError, UserNotFoundError):
            raise AuthorizationError('Token verification failed')
