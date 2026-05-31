import bcrypt
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.models.users import Base, Users
from app.models.posts import Posts
from dependencies.db import get_session
from main import app


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    u = Users(
        username='joao',
        email='joao@gmail.com',
        password=hash_password('234hj45'),
        phone_number='35999876765',
        first_name='João',
        last_name='Pedro',
        gender='male'
    )
    session.add(u)
    session.commit()
    session.refresh(u)
    return u


@pytest.fixture
def token(user, client):
    login_data = {"username": "joao", "password": "234hj45"}
    response = client.post("/api/v1/login", data=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_user(session):
    u = Users(
        username='admin_user',
        email='admin@gmail.com',
        password=hash_password('adminpass123'),
        phone_number='35999000001',
        first_name='Admin',
        last_name='User',
        gender='male',
        role='admin'
    )
    session.add(u)
    session.commit()
    session.refresh(u)
    return u


@pytest.fixture
def admin_token(admin_user, client):
    login_data = {"username": "admin_user", "password": "adminpass123"}
    response = client.post("/api/v1/login", data=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def post(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/api/v1/posts/",
        data={"title": "Post Fixture", "content": "Conteúdo do fixture"},
        files={},
        headers=headers
    )
    assert response.status_code == 201
    return response.json()["result"]


@pytest.fixture
def make_user(session):
    """Factory fixture para criar usuários adicionais."""
    created = []

    def _make(username, email, phone_number, password="testpass123", role="user"):
        u = Users(
            username=username,
            email=email,
            password=hash_password(password),
            phone_number=phone_number,
            first_name="Test",
            last_name="User",
            gender="male",
            role=role
        )
        session.add(u)
        session.commit()
        session.refresh(u)
        created.append(u)
        return u

    return _make
