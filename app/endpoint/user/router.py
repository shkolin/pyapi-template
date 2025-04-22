from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends

from app.command.user.create_user import CreateUserCommand
from app.command.user.email import ConfirmEmailCommand
from app.command.user.password import RecoverPasswordCommand
from app.command.user.password import ResetPasswordRequestCommand
from app.container import AppContainer
from app.endpoint.response import GeneralSuccessResponse
from app.endpoint.user.request import CreateUserRequest
from app.endpoint.user.request import RecoverPasswordRequest
from app.endpoint.user.request import ResetPasswordRequest
from app.handler.interface import CommandHandlerInterface

router = APIRouter()


@router.post('/users', response_model=GeneralSuccessResponse)
@inject
def create_user(
        request: CreateUserRequest,
        handler: CommandHandlerInterface[CreateUserCommand, None] = Depends(
            Provide[AppContainer.handler.create_user]
        )
) -> GeneralSuccessResponse:
    handler.handle(CreateUserCommand(**request.model_dump()))
    return GeneralSuccessResponse()


@router.post('/reset-password-request', response_model=GeneralSuccessResponse)
@inject
def reset_password_request(
        request: ResetPasswordRequest,
        handler: CommandHandlerInterface[ResetPasswordRequestCommand, None] = Depends(
            Provide[AppContainer.handler.reset_password_request]
        )
) -> GeneralSuccessResponse:
    handler.handle(ResetPasswordRequestCommand(**request.model_dump()))
    return GeneralSuccessResponse()


@router.post('/recover-password', response_model=GeneralSuccessResponse)
@inject
def recover_password(
        request: RecoverPasswordRequest,
        handler: CommandHandlerInterface[RecoverPasswordCommand, None] = Depends(
            Provide[AppContainer.handler.recover_password]
        )
) -> GeneralSuccessResponse:
    handler.handle(RecoverPasswordCommand(**request.model_dump()))
    return GeneralSuccessResponse()


@router.post('/confirm-email', response_model=GeneralSuccessResponse)
@inject
def confirm_email(
        token: str = Body(embed=True),
        handler: CommandHandlerInterface[ConfirmEmailCommand, None] = Depends(
            Provide[AppContainer.handler.confirm_email]
        )
) -> GeneralSuccessResponse:
    handler.handle(ConfirmEmailCommand(token=token))
    return GeneralSuccessResponse()
