from abc import ABC
from abc import abstractmethod

from jinja2 import Template


class MailerInterface(ABC):
    @abstractmethod
    def send_message(self, subject: str, recipient: str, body: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_template(self, name: str) -> Template:
        raise NotImplementedError
