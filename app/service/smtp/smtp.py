import smtplib
import ssl
import threading
from email.message import Message
from typing import Optional

from app.service.smtp.exception import SMTPClientError
from app.service.smtp.interface import SMTPClientInterface


class SMTPClient(SMTPClientInterface):
    def __init__(
            self,
            host: str,
            port: int,
            username: str,
            password: str,
            use_tls: bool,
            fail_silently: bool = False,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.fail_silently = fail_silently
        self.connection: Optional[smtplib.SMTP] = None
        self._lock = threading.RLock()

    def __open(self) -> bool:
        if self.connection:
            return False
        try:
            self.connection = smtplib.SMTP(self.host, self.port)
            if self.use_tls:
                self.connection.starttls()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except OSError:
            if not self.fail_silently:
                raise SMTPClientError

        return False

    def __close(self) -> None:
        if self.connection is None:
            return
        try:
            try:
                self.connection.quit()
            except (ssl.SSLError, smtplib.SMTPServerDisconnected):
                self.connection.close()
            except smtplib.SMTPException:
                if self.fail_silently:
                    return
                raise SMTPClientError
        finally:
            self.connection = None

    def __send(self, email_message: Message) -> bool:
        if self.connection is None:
            raise
        try:
            self.connection.send_message(email_message)
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise SMTPClientError
            return False
        return True

    def send_messages(self, email_messages: list[Message]) -> int:
        if not email_messages:
            return 0
        with self._lock:
            new_conn_created = self.__open()
            if not self.connection or new_conn_created is None:
                return 0
            num_sent = 0
            try:
                for message in email_messages:
                    sent = self.__send(message)
                    if sent:
                        num_sent += 1
            finally:
                if new_conn_created:
                    self.__close()

        return num_sent
