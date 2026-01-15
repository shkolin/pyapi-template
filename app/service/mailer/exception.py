from app.exception import BaseRuntimeError


class MailerError(BaseRuntimeError):
    message = 'Failed to send email message'
