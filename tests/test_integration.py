import pytest
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

# ==========================================
# 1. TESTES DE SAÚDE E INFRAESTRUTURA
# ==========================================

def test_integracao_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data.get("status") == "healthy"
    assert data.get("database") == "connected"

def test_integracao_rota_nao_encontrada():
    response = client.get("/api/v1/rota-fantasma")
    assert response.status_code == 404

# ==========================================
# 2. TESTES DE INTEGRAÇÃO DE USUÁRIOS E AUTENTICAÇÃO
# ==========================================

test_data = {}

def test_integracao_criar_usuario():
    payload = {
        "username": "integracao_user",
        "email": "integracao@blog.com",
        "password": "senha_segura_123",
        "role": "admin"
    }
    response = client.post("/users", json=payload)
    
    # Pode retornar 200 ou 201
    assert response.status_code in [200, 201] 
    
    data = response.json()
    assert "id" in data
    assert data["username"] == payload["username"]

def test_integracao_login_obter_token():
    payload = {
        "username": "integracao@blog.com", # OAuth2 usa o email no campo username (não sei o por quê)
        "password": "senha_segura_123"
    }
    response = client.post("/login", data=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    test_data["token"] = data["access_token"]

def test_integracao_login_falha_credenciais_invalidas():
    payload = {"username": "fake@blog.com", "password": "wrongpassword"}
    response = client.post("/login", data=payload)
    assert response.status_code in [401, 403, 404]

# ==========================================
# 3. TESTES DE INTEGRAÇÃO DO BLOG (REQUER AUTENTICAÇÃO)
# ==========================================

def test_integracao_criar_post_no_blog():
    headers = {
        "Authorization": f"Bearer {test_data.get('token')}"
    }
    payload = {
        "title": "Primeiro Post de Integração",
        "content": "Este post foi gerado automaticamente pelo pytest no pipeline CI/CD.",
        "published": True
    }
    
    response = client.post("/posts", json=payload, headers=headers)
    assert response.status_code in [200, 201]
    
    data = response.json()
    assert "id" in data
    assert data["title"] == payload["title"]
    
    test_data["post_id"] = data["id"]

def test_integracao_listar_posts():
    response = client.get("/posts")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    post_ids = [post["id"] for post in data]
    assert test_data["post_id"] in post_ids

def test_integracao_criar_post_sem_autenticacao():
    payload = {
        "title": "Post Hacker",
        "content": "Tentando invadir o blog."
    }
    response = client.post("/posts", json=payload)
    assert response.status_code == 401