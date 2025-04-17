from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def unauthorized_exception_handler(_: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder({'detail': {'error': str(exc)}}),
        headers={'WWW-Authenticate': 'Bearer'},
    )


def domain_error_handler(_: Request, exc: Exception) -> Response:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({'detail': {'error': str(exc)}}),
    )
