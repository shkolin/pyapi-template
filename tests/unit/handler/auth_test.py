from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.command.auth import AuthorizationViaCredentialsCommand
from app.endpoint.auth.response import Token
from app.endpoint.exception import AuthorizationError
from app.exception import DomainError
from app.handler.auth import AuthorizationViaCredentialsCommandHandler
from app.repository.exception import PersistenceError
from app.repository.user.exception import UserNotFoundError
from app.repository.user.user import UserRepository
from app.service.jwt.exception import JWTServiceError
from app.service.jwt.interface import JWTServiceInterface
from app.uow import UnitOfWorkInterface


class TestAuthorizationViaCredentialsCommandHandler:
    @pytest.fixture
    def mock_uow(self) -> MagicMock:
        return MagicMock(spec=UnitOfWorkInterface)

    @pytest.fixture
    def mock_jwt_service(self) -> MagicMock:
        return MagicMock(spec=JWTServiceInterface)

    @pytest.fixture
    def mock_user(self) -> MagicMock:
        user = MagicMock()
        user.is_active = True
        user.email_verified = True
        user.id = 123
        user.verify_password.return_value = True
        user.update_last_login_date = MagicMock()
        return user

    @pytest.fixture
    def mock_user_repository(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def handler(
        self, mock_uow: MagicMock, mock_jwt_service: MagicMock
    ) -> AuthorizationViaCredentialsCommandHandler:
        return AuthorizationViaCredentialsCommandHandler(mock_uow, mock_jwt_service)

    @pytest.fixture
    def command(self) -> AuthorizationViaCredentialsCommand:
        return AuthorizationViaCredentialsCommand(
            login='test@example.com', plain_password='P@$$w0rd'
        )

    def test_handle_success(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_jwt_service: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        mock_token_data = MagicMock()
        mock_token_data.model_dump.return_value = {
            'access_token': 'test_token',
            'token_type': 'bearer',
        }
        mock_jwt_service.encode.return_value = mock_token_data

        result = handler.handle(command)

        assert isinstance(result, Token)
        assert result.access_token == 'test_token'
        assert result.token_type == 'bearer'

        mock_uow.get_repository.assert_called_once_with(UserRepository)
        mock_user_repository.get_by_login.assert_called_once_with('test@example.com')
        mock_user.verify_password.assert_called_once_with('P@$$w0rd')
        mock_user.update_last_login_date.assert_called_once()
        mock_jwt_service.encode.assert_called_once_with(123)

    def test_handle_user_not_found_raises_domain_error(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_user_repository: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.side_effect = UserNotFoundError()

        with pytest.raises(DomainError) as exc_info:
            handler.handle(command)

        assert str(exc_info.value) == 'Failed to authorization'
        mock_user_repository.get_by_login.assert_called_once_with('test@example.com')

    def test_handle_inactive_user_raises_domain_error(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_user.is_active = False
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        with pytest.raises(DomainError) as exc_info:
            handler.handle(command)

        assert str(exc_info.value) == 'Failed to authorization'
        mock_user.verify_password.assert_not_called()

    def test_handle_invalid_password_raises_domain_error(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_user.verify_password.return_value = False
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        with pytest.raises(DomainError) as exc_info:
            handler.handle(command)

        assert str(exc_info.value) == 'Failed to authorization'
        mock_user.verify_password.assert_called_once_with('P@$$w0rd')
        mock_user.update_last_login_date.assert_not_called()

    def test_handle_email_not_verified_raises_domain_error(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_user.email_verified = False
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        with pytest.raises(DomainError) as exc_info:
            handler.handle(command)

        assert str(exc_info.value) == 'Failed to authorization'
        mock_user.verify_password.assert_called_once_with('P@$$w0rd')
        mock_user.update_last_login_date.assert_not_called()

    def test_handle_persistence_error_raises_domain_error(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        mock_uow.__exit__.return_value = None
        mock_uow.__exit__.side_effect = PersistenceError('Database error')

        with pytest.raises(DomainError) as exc_info:
            handler.handle(command)

        assert str(exc_info.value) == 'Failed to authorization'

    def test_handle_jwt_service_error_propagates(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_jwt_service: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        mock_jwt_service.encode.side_effect = JWTServiceError('JWT encoding failed')

        with pytest.raises(JWTServiceError) as exc_info:
            handler.handle(command)

        assert str(exc_info.value) == 'JWT encoding failed'
        mock_user.update_last_login_date.assert_called_once()

    def test_handle_authorization_error_with_custom_message(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        custom_error = AuthorizationError('Custom auth error')
        mock_user.verify_password.side_effect = custom_error

        with pytest.raises(DomainError) as exc_info:
            handler.handle(command)

        assert str(exc_info.value) == 'Failed to authorization'

    def test_handler_initialization(
        self,
        mock_uow: MagicMock,
        mock_jwt_service: MagicMock,
    ) -> None:
        handler = AuthorizationViaCredentialsCommandHandler(mock_uow, mock_jwt_service)

        assert handler is not None

    def test_handle_calls_uow_context_manager(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_jwt_service: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
        command: AuthorizationViaCredentialsCommand,
    ) -> None:
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        mock_token_data = MagicMock()
        mock_token_data.model_dump.return_value = {
            'access_token': 'test_token',
            'token_type': 'bearer',
        }
        mock_jwt_service.encode.return_value = mock_token_data

        handler.handle(command)

        mock_uow.__enter__.assert_called_once()
        mock_uow.__exit__.assert_called_once()

    def test_handle_with_different_command_values(
        self,
        handler: AuthorizationViaCredentialsCommandHandler,
        mock_uow: MagicMock,
        mock_jwt_service: MagicMock,
        mock_user_repository: MagicMock,
        mock_user: MagicMock,
    ) -> None:
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.get_repository.return_value = mock_user_repository
        mock_user_repository.get_by_login.return_value = mock_user

        mock_token_data = MagicMock()
        mock_token_data.model_dump.return_value = {
            'access_token': 'different_token',
            'token_type': 'bearer',
        }
        mock_jwt_service.encode.return_value = mock_token_data

        command = AuthorizationViaCredentialsCommand(
            login='different@example.com', plain_password='DifferentP@$$w0rd'
        )

        result = handler.handle(command)

        assert result.access_token == 'different_token'
        mock_user_repository.get_by_login.assert_called_once_with(
            'different@example.com'
        )
        mock_user.verify_password.assert_called_once_with('DifferentP@$$w0rd')
