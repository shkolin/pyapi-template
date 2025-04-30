from uuid import UUID

from sqlalchemy import select

from app.domain.user.login import LoginResetRequest
from app.domain.user.password import PasswordResetRequest
from app.domain.user.user import User
from app.mapping.user import LoginResetRequestTable
from app.mapping.user import PasswordResetRequestTable
from app.mapping.user import UserTable
from app.repository.base import BaseRepository
from app.repository.user.exception import LoginResetRequestNotFoundError
from app.repository.user.exception import PasswordResetRequestNotFoundError
from app.repository.user.exception import UserNotFoundError
from app.repository.user.interface import UserRepositoryInterface


class UserRepository(BaseRepository[User], UserRepositoryInterface):
    def get_by_id(self, obj_id: UUID) -> User:
        found: User | None = self._session.get(User, obj_id)
        if not found:
            raise UserNotFoundError
        return found

    def get_by_login(self, login: str) -> User:
        found = self._session.execute(
            select(User).where(UserTable.c.email == login)
        ).scalar_one_or_none()
        if not found:
            raise UserNotFoundError
        return found

    def get_password_reset_request(self, token: str) -> PasswordResetRequest:
        found = self._session.execute(
            select(PasswordResetRequest).where(
                PasswordResetRequestTable.c.token == token,
                PasswordResetRequestTable.c.is_used.is_not(True)
            )
        ).scalar_one_or_none()
        if not found:
            raise PasswordResetRequestNotFoundError
        return found

    def get_login_reset_request(self, token: str) -> LoginResetRequest:
        found = self._session.execute(
            select(LoginResetRequest).where(
                LoginResetRequestTable.c.token == token,
                LoginResetRequestTable.c.is_used.is_not(True)
            )
        ).scalar_one_or_none()
        if not found:
            raise LoginResetRequestNotFoundError
        return found
