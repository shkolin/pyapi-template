from pydantic import BaseModel


class GeneralSuccessResponse(BaseModel):
    status: str = 'OK'
