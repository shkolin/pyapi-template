from pydantic import BaseModel
from pydantic import ConfigDict


class BaseCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
