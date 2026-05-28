from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from jose import jwt as jose_jwt

from app.repositories.jwt_repo import JWTRepo
from config import SECRET_KEY, ALGORITHM
from dependencies.auth import get_admin_user_dependency, get_current_user_dependency


def make_mock_user(user_id=1, role="user"):
    user = MagicMock()
    user.id = user_id
    user.role = role
    return user


def make_mock_db(user=None):
    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = user
    return mock_db


class TestGetCurrentUserDependency:
    def test_valid_token_returns_user(self):
        db_user = make_mock_user(user_id=5)
        token_user = make_mock_user(user_id=5)
        token = JWTRepo.generate_token(token_user)
        mock_db = make_mock_db(user=db_user)

        result = get_current_user_dependency(db=mock_db, token=token)
        assert result.id == 5

    def test_invalid_token_raises_forbidden(self):
        mock_db = make_mock_db()
        with pytest.raises(HTTPException) as exc_info:
            get_current_user_dependency(db=mock_db, token="invalid.token.here")
        assert exc_info.value.status_code == 403

    def test_token_without_sub_raises_401(self):
        token_without_sub = jose_jwt.encode(
            {"exp": datetime.utcnow() + timedelta(minutes=15), "role": "user"},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        mock_db = make_mock_db()
        with pytest.raises(HTTPException) as exc_info:
            get_current_user_dependency(db=mock_db, token=token_without_sub)
        assert exc_info.value.status_code == 401

    def test_user_not_in_db_raises_404(self):
        token_user = make_mock_user(user_id=99)
        token = JWTRepo.generate_token(token_user)
        mock_db = make_mock_db(user=None)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user_dependency(db=mock_db, token=token)
        assert exc_info.value.status_code == 404


class TestGetAdminUserDependency:
    def test_admin_user_is_returned(self):
        admin = make_mock_user(user_id=1, role="admin")
        result = get_admin_user_dependency(current_user=admin)
        assert result.role == "admin"

    def test_regular_user_raises_forbidden(self):
        regular = make_mock_user(user_id=2, role="user")
        with pytest.raises(HTTPException) as exc_info:
            get_admin_user_dependency(current_user=regular)
        assert exc_info.value.status_code == 403
