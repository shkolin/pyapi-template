class PersistenceError(RuntimeError):
    pass


class UserNotFoundError(RuntimeError):
    pass


class PasswordResetRequestNotFoundError(RuntimeError):
    pass


class LoginResetRequestNotFoundError(RuntimeError):
    pass
