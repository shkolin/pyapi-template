from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Optional

from jinja2 import Template

from app.service.mailer.interface import MailerInterface
from app.service.smtp.interface import SMTPClientInterface
from app.service.templater.interface import TemplaterInterface


class Mailer(MailerInterface):
    def __init__(
            self,
            smtp: SMTPClientInterface,
            templater: TemplaterInterface,
            from_email: str,
            from_name: Optional[str] = None
    ) -> None:
        self.__smtp = smtp
        self.__templater = templater
        self.__from_email = from_email
        self.__from_name = from_name

    def send_message(self, subject: str, recipient: str, body: str) -> None:
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = self._format_from()
        message['To'] = recipient

        message.attach(MIMEText(body, 'html'))

        self.__smtp.send_messages([message])

    def _format_from(self) -> str:
        if self.__from_name:
            return formataddr((self.__from_name, self.__from_email))
        return self.__from_email

    def get_template(self, name: str) -> Template:
        return self.__templater.get_template(f'email/{name}')
