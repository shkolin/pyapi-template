from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Template

from app.service.mailer.interface import MailerInterface
from app.service.smtp.interface import SMTPClientInterface
from app.service.templater.interface import TemplaterInterface


class Mailer(MailerInterface):
    def __init__(
            self,
            smtp: SMTPClientInterface,
            templater: TemplaterInterface,
            service_email: str,
            project_name: str
    ) -> None:
        self.__smtp = smtp
        self.__templater = templater
        self.__service_email = service_email
        self.__project_name = project_name

    def send_message(self, subject: str, recipient: str, body: str) -> None:
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = f'{self.__project_name} <{self.__service_email}>'
        message['To'] = recipient

        message.attach(MIMEText(body, 'html'))

        self.__smtp.send_messages([message])

    def get_template(self, name: str) -> Template:
        return self.__templater.get_template(f'email/{name}')
