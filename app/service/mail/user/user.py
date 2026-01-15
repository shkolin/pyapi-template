from app.service.mail.user.interface import UserMailServiceInterface
from app.service.mailer.interface import MailerInterface


class UserMailService(UserMailServiceInterface):
    def __init__(self, mailer: MailerInterface):
        self.__mailer = mailer

    def send_password_reset(self, to: str, username: str, token: str) -> None:
        tpl = self.__mailer.get_template('reset_password_request')
        self.__mailer.send_message('Reset Password', to, tpl.render(username=username, token=token))

    def send_welcome(self, to: str, username: str) -> None:
        tpl = self.__mailer.get_template('welcome')
        self.__mailer.send_message('Welcome', to, tpl.render(username=username))

    def send_login_reset(self, to: str, username: str, token: str) -> None:
        tpl = self.__mailer.get_template('reset_login_request')
        self.__mailer.send_message('Reset Login', to, tpl.render(username=username, token=token))

    def send_email_confirmation(self, to: str, username: str, token: str) -> None:
        tpl = self.__mailer.get_template('confirm_email')
        self.__mailer.send_message('Confirm email', to, tpl.render(username=username, token=token))
