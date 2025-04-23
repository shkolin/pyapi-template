from app.event.interface import EventInterface


class UserEvent(EventInterface):
    REGISTERED = 'user_registered'
    RESET_PASSWORD_REQUESTED = 'user_reset_password_requested'
    RESET_LOGIN_REQUESTED = 'user_reset_login_requested'
