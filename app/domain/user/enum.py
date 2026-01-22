from enum import StrEnum
from enum import auto


class UserStatus(StrEnum):
    ACTIVE = auto()
    DELETED = auto()


class TokenStatus(StrEnum):
    PENDING = auto()
    USED = auto()
    CANCELED = auto()
    EXPIRED = auto()
