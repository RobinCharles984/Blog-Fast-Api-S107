def test_create_user(client):
    user_data = {
        "username": "joao",
        "email": "joao@gmail.com",
        "password": "234hj45",
        "phone_number": "35999876765",
        "first_name": "João",
        "last_name": "Pedro",
        "gender": "M"
    }

    response = client.post("/api/v1/signup/", json=user_data)

    assert response.status_code == 201

    data = response.json()
    assert data['result']['username'] == 'joao'
    assert data['result']['email'] == 'joao@gmail.com'
    assert data['message'] == "User registered successfully"


def test_login_user(client):
    user_data = {
        "username": "Rogerio",
        "email": "roger@gmail.com",
        "password": "456908kl",
        "phone_number": "35999873765",
        "first_name": "Rogerio",
        "last_name": "Freire",
        "gender": "M"
    }

    response = client.post("/api/v1/signup/", json=user_data)
    assert response.status_code == 201

    login_data = {"username": "Rogerio", "password": "456908kl"}
    login_response = client.post("/api/v1/login/", data=login_data)

    assert login_response.status_code == 200
    data = login_response.json()
    assert data['access_token'] != ""
    assert data['token_type'] == 'bearer'


def test_signup_duplicate_username(client):
    user_data = {
        "username": "dupuser",
        "email": "dup1@gmail.com",
        "password": "pass1234",
        "phone_number": "35999111001",
        "first_name": "Dup",
        "last_name": "User",
        "gender": "M"
    }
    client.post("/api/v1/signup/", json=user_data)

    user_data["email"] = "dup2@gmail.com"
    user_data["phone_number"] = "35999111002"
    response = client.post("/api/v1/signup/", json=user_data)

    assert response.status_code == 400
    assert "Username already exists" in response.json()["detail"]


def test_signup_duplicate_email(client):
    user_data = {
        "username": "emailuser1",
        "email": "same@gmail.com",
        "password": "pass1234",
        "phone_number": "35999222001",
        "first_name": "Email",
        "last_name": "User",
        "gender": "M"
    }
    client.post("/api/v1/signup/", json=user_data)

    user_data["username"] = "emailuser2"
    user_data["phone_number"] = "35999222002"
    response = client.post("/api/v1/signup/", json=user_data)

    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]


def test_login_wrong_password(client):
    user_data = {
        "username": "wrongpass",
        "email": "wrongpass@gmail.com",
        "password": "correctpass",
        "phone_number": "35999333001",
        "first_name": "Wrong",
        "last_name": "Pass",
        "gender": "M"
    }
    client.post("/api/v1/signup/", json=user_data)

    login_response = client.post("/api/v1/login/", data={"username": "wrongpass", "password": "wrongpass"})
    assert login_response.status_code == 400
    assert "Invalid Password" in login_response.json()["detail"]


def test_login_user_not_found(client):
    login_response = client.post("/api/v1/login/", data={"username": "ghost_user", "password": "anypass"})
    assert login_response.status_code == 400
    assert "Invalid credentials" in login_response.json()["detail"]


def test_promote_user_as_admin(client, user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.patch(f"/api/v1/{user.id}/promote", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["role"] == "admin"
    assert data["result"]["user"] == "joao"


def test_promote_user_as_regular_user(client, user, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.patch(f"/api/v1/{user.id}/promote", headers=headers)
    assert response.status_code == 403


def test_promote_nonexistent_user(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.patch("/api/v1/99999/promote", headers=headers)
    assert response.status_code == 404
