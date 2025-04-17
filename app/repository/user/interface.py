from abc import ABC
from abc import abstractmethod
from uuid import UUID

from app.domain.user.login import LoginResetRequest
from app.domain.user.password import PasswordResetRequest
from app.domain.user.user import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, obj_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_login(self, login: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_password_reset_request(self, token: str) -> PasswordResetRequest:
        raise NotImplementedError

    @abstractmethod
    def get_login_reset_request(self, token: str) -> LoginResetRequest:
        raise NotImplementedError
