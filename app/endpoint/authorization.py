from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.command.auth import AuthorizationViaTokenCommand
from app.container import AppContainer
from app.domain.user.user import User
from app.endpoint.exception import AuthorizationError
from app.handler.interface import CommandHandlerInterface

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth', auto_error=False)


@inject
def authorization_via_token(
        token: str = Depends(oauth2_scheme),
        handler: CommandHandlerInterface[AuthorizationViaTokenCommand, User] = Depends(
            Provide[AppContainer.handler.authorization_via_token]
        )
) -> User:
    if not token:
        raise AuthorizationError('Missing authorization token')
    return handler.handle(AuthorizationViaTokenCommand(token=token))
