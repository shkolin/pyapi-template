from enum import StrEnum
from enum import auto


class TokenStatus(StrEnum):
    PENDING = auto()
    USED = auto()
    CANCELED = auto()
    EXPIRED = auto()
