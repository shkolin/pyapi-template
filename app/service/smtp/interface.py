from abc import ABC
from abc import abstractmethod
from email.message import Message


class SMTPClientInterface(ABC):
    @abstractmethod
    def send_messages(self, email_messages: list[Message]) -> int:
        raise NotImplementedError
