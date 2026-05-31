import pytest
from unittest.mock import MagicMock
from jose import JWTError

from app.repositories.jwt_repo import JWTRepo
from config import SECRET_KEY, ALGORITHM
from jose import jwt as jose_jwt


def make_mock_user(user_id=1, role="user"):
    user = MagicMock()
    user.id = user_id
    user.role = role
    return user


class TestJWTRepo:
    def test_generate_token_returns_non_empty_string(self):
        user = make_mock_user()
        token = JWTRepo.generate_token(user)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_generate_token_payload_contains_sub(self):
        user = make_mock_user(user_id=42)
        token = JWTRepo.generate_token(user)
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "42"

    def test_generate_token_payload_contains_role(self):
        user = make_mock_user(role="admin")
        token = JWTRepo.generate_token(user)
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["role"] == "admin"

    def test_generate_token_payload_contains_exp(self):
        user = make_mock_user()
        token = JWTRepo.generate_token(user)
        payload = jose_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in payload

    def test_decode_token_valid_returns_payload(self):
        user = make_mock_user(user_id=7)
        token = JWTRepo.generate_token(user)
        payload = JWTRepo.decode_token(token)
        assert payload["sub"] == "7"

    def test_decode_token_invalid_raises_jwt_error(self):
        with pytest.raises(JWTError):
            JWTRepo.decode_token("this.is.not.a.valid.token")

    def test_decode_token_tampered_raises_jwt_error(self):
        user = make_mock_user()
        token = JWTRepo.generate_token(user)
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(JWTError):
            JWTRepo.decode_token(tampered)
