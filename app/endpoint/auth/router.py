from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.command.auth import AuthorizationViaCredentialsCommand
from app.container import AppContainer
from app.endpoint.auth.response import TokenResponse
from app.handler.interface import CommandHandlerInterface

router = APIRouter()


@router.post('/auth', response_model=TokenResponse)
@inject
def authorization_via_credentials(
        form_data: OAuth2PasswordRequestForm = Depends(),
        handler: CommandHandlerInterface[
            AuthorizationViaCredentialsCommand, TokenResponse
        ] = Depends(Provide[AppContainer.handler.authorization_via_credentials])
) -> TokenResponse:
    return handler.handle(
        AuthorizationViaCredentialsCommand(
            login=form_data.username, plain_password=form_data.password
        )
    )
