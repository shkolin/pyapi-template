import smtplib
import ssl
import threading
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Optional

from jinja2 import Template

from app.service.mailer.exception import MailerError
from app.service.mailer.interface import MailerInterface
from app.service.templater.interface import TemplaterInterface


class SMTPClient(MailerInterface):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool,
        templater: TemplaterInterface,
        from_email: str,
        from_name: Optional[str] = None,
        fail_silently: bool = False,
    ) -> None:
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__use_tls = use_tls
        self.__fail_silently = fail_silently
        self.__connection: Optional[smtplib.SMTP] = None
        self.__lock = threading.RLock()
        self.__templater = templater
        self.__from_email = from_email
        self.__from_name = from_name

    def __open(self) -> bool:
        if self.__connection:
            return False
        try:
            self.__connection = smtplib.SMTP(self.__host, self.__port)
            if self.__use_tls:
                self.__connection.starttls()
            if self.__username and self.__password:
                self.__connection.login(self.__username, self.__password)
            return True
        except OSError:
            if not self.__fail_silently:
                raise MailerError

        return False

    def __close(self) -> None:
        if self.__connection is None:
            return
        try:
            try:
                self.__connection.quit()
            except (ssl.SSLError, smtplib.SMTPServerDisconnected):
                self.__connection.close()
            except smtplib.SMTPException:
                if self.__fail_silently:
                    return
                raise MailerError
        finally:
            self.__connection = None

    def __send(self, email_message: Message) -> bool:
        if self.__connection is None:
            raise
        try:
            self.__connection.send_message(email_message)
        except smtplib.SMTPException:
            if not self.__fail_silently:
                raise MailerError
            return False
        return True

    def __send_messages(self, email_messages: list[Message]) -> int:
        if not email_messages:
            return 0

        with self.__lock:
            new_conn_created = self.__open()
            if not self.__connection or new_conn_created is None:
                return 0
            num_sent = 0

            try:
                for message in email_messages:
                    sent = self.__send(message)
                    if sent:
                        num_sent += 1
                return num_sent
            finally:
                if new_conn_created:
                    self.__close()

    def send_message(self, subject: str, recipient: str, body: str) -> None:
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = self._format_from()
        message['To'] = recipient

        message.attach(MIMEText(body, 'html'))

        self.__send_messages([message])

    def _format_from(self) -> str:
        if self.__from_name:
            return formataddr((self.__from_name, self.__from_email))
        return self.__from_email

    def get_template(self, name: str) -> Template:
        return self.__templater.get_template(f'email/{name}')
