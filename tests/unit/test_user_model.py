from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

from argon2 import PasswordHasher

from app.domain.user.enum import UserStatus
from app.domain.user.login import LoginResetRequest
from app.domain.user.password import PasswordResetRequest
from app.domain.user.user import User
from app.value_object.user import UserEmail
from app.value_object.user import UserName
from app.value_object.user import UserPassword


def test_user_initialization_with_required_fields() -> None:
    name = UserName('John Doe')
    email = UserEmail('john@example.com')
    password = UserPassword('secure_password123')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed_password'
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)

        assert user.name == 'John Doe'
        assert user.email == 'john@example.com'
        assert user.password_hash == 'hashed_password'
        assert user.status == UserStatus.ACTIVE.value
        assert user.email_verified is False
        assert user.created_at is not None
        assert user.updated_at is None
        assert user.last_login_date is None


def test_user_password_is_hashed() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    password = UserPassword('plaintext_password')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'argon2_hash_output'
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)

        assert user.password_hash == 'argon2_hash_output'
        mock_hasher_instance.hash.assert_called_once_with('plaintext_password')


def test_verify_password_success() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    password = UserPassword('correct_password')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed_password'
        mock_hasher_instance.verify.return_value = True
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)
        result = user.verify_password('correct_password')

        assert result is True
        mock_hasher_instance.verify.assert_called_once_with(
            'hashed_password',
            'correct_password',
        )


def test_verify_password_failure() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    password = UserPassword('correct_password')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed_password'
        mock_hasher_instance.verify.return_value = False
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)
        result = user.verify_password('wrong_password')

        assert result is False


def test_update_last_login_date() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    password = UserPassword('password123')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed'
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)
        assert user.last_login_date is None

        user.update_last_login_date()

        assert user.last_login_date is not None
        assert isinstance(user.last_login_date, datetime)


def test_update_last_modified_date() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    password = UserPassword('password123')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed'
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)
        assert user.updated_at is None

        user.update_last_modified_date()

        assert user.updated_at is not None
        assert isinstance(user.updated_at, datetime)


def test_update_password() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    old_password = UserPassword('old_password')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.side_effect = [
            'old_hashed_password',
            'new_hashed_password',
        ]
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, old_password)
        original_hash = user.password_hash

        new_password = UserPassword('new_password')
        user.update_password(new_password)

        assert user.password_hash != original_hash
        assert user.password_hash == 'new_hashed_password'
        assert mock_hasher_instance.hash.call_count == 2


def test_update_email() -> None:
    name = UserName('Test User')
    email = UserEmail('old@example.com')
    password = UserPassword('password123')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed'
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)
        assert user.email == 'old@example.com'

        new_email = UserEmail('new@example.com')
        user.update_email(new_email)

        assert user.email == 'new@example.com'


def test_confirm_email() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    password = UserPassword('password123')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed'
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)
        assert user.email_verified is False

        user.confirm_email()

        assert user.email_verified is True


def test_reset_password_request() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    password = UserPassword('password123')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed'
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)

        request = user.reset_password_request()

        assert isinstance(request, PasswordResetRequest)
        assert request in user.password_reset_requests


def test_reset_login_request() -> None:
    name = UserName('Test User')
    email = UserEmail('test@example.com')
    password = UserPassword('password123')

    with patch.object(User, '_User__password_hasher') as mock_hasher:
        mock_hasher_instance = MagicMock(spec=PasswordHasher)
        mock_hasher_instance.hash.return_value = 'hashed'
        mock_hasher.return_value = mock_hasher_instance

        user = User(name, email, password)
        user.confirm_email()
        assert user.email_verified is True

        new_email = UserEmail('new@example.com')
        request = user.reset_login_request(new_email)

        assert user.email_verified is False

        assert isinstance(request, LoginResetRequest)
        assert request in user.login_reset_requests
