from abc import ABC
from abc import abstractmethod


class UserMailServiceInterface(ABC):
    @abstractmethod
    def send_password_reset(
            self, to: str, username: str, token: str
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_welcome(self, to: str, username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_login_reset(self, to: str, username: str, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_email_confirmation(self, to: str, username: str, token: str) -> None:
        raise NotImplementedError
