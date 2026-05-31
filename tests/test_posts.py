from io import BytesIO
from unittest.mock import patch, MagicMock

BASE = "/api/v1"


def get_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_post(client, token, title="Post Padrão", content="Conteúdo padrão"):
    headers = get_headers(token)
    post_data = {"title": title, "content": content}
    response = client.post(f"{BASE}/posts/", data=post_data, files={}, headers=headers)
    assert response.status_code == 201
    return response.json()['result']


# ---------------------------------------------------------------------------
# Happy path tests
# ---------------------------------------------------------------------------

def test_create_post(client, token):
    post = create_post(client, token, title="Teste de POST", content="ISSO É APENAS TESTE")
    assert post["title"] == "Teste de POST"


def test_get_post(client, token):
    post = create_post(client, token, title="Post para GET", content="Conteúdo de teste para GET")

    response = client.get(f"{BASE}/posts?post_id={post['id']}", headers=get_headers(token))
    assert response.status_code == 200
    assert response.json()['result']['title'] == "Post para GET"


def test_delete_post(client, token):
    post = create_post(client, token, title="Post para DELETE", content="Conteúdo para DELETE")

    delete_response = client.delete(f"{BASE}/posts/{post['id']}", headers=get_headers(token))
    assert delete_response.status_code == 204

    get_response = client.get(f"{BASE}/posts?post_id={post['id']}", headers=get_headers(token))
    assert get_response.status_code == 404


def test_update_post(client, token):
    post = create_post(client, token, title="Post original", content="Conteúdo original")

    update_response = client.put(
        f"{BASE}/posts/{post['id']}",
        data={"title": "Post atualizado", "content": "Novo conteúdo editado"},
        files={},
        headers=get_headers(token)
    )
    assert update_response.status_code == 200
    assert update_response.json()["result"]["title"] == "Post atualizado"


# ---------------------------------------------------------------------------
# Auth error tests
# ---------------------------------------------------------------------------

def test_create_post_without_auth(client):
    response = client.post(f"{BASE}/posts/", data={"title": "No auth", "content": "x"}, files={})
    assert response.status_code in (401, 403)


def test_get_posts_without_auth(client):
    response = client.get(f"{BASE}/posts")
    assert response.status_code in (401, 403)


# ---------------------------------------------------------------------------
# GET posts variation tests
# ---------------------------------------------------------------------------

def test_get_all_posts_returns_list(client, token):
    create_post(client, token, title="Lista 1", content="C1")
    create_post(client, token, title="Lista 2", content="C2")

    response = client.get(f"{BASE}/posts", headers=get_headers(token))
    assert response.status_code == 200
    assert isinstance(response.json()["result"], list)


def test_get_posts_with_pagination_params(client, token):
    for i in range(5):
        create_post(client, token, title=f"Page {i}", content="content")

    response = client.get(f"{BASE}/posts?skip=0&limit=2", headers=get_headers(token))
    assert response.status_code == 200
    assert len(response.json()["result"]) == 2


def test_get_nonexistent_post_returns_404(client, token):
    response = client.get(f"{BASE}/posts?post_id=99999", headers=get_headers(token))
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Delete error tests
# ---------------------------------------------------------------------------

def test_delete_nonexistent_post_returns_404(client, token):
    response = client.delete(f"{BASE}/posts/99999", headers=get_headers(token))
    assert response.status_code == 404


def test_delete_post_by_non_owner_returns_403(client, token, make_user):
    post = create_post(client, token, title="Owner's post", content="content")

    other_user_data = {
        "username": "other_person",
        "email": "other@gmail.com",
        "password": "otherpass123",
        "phone_number": "35900099901",
        "first_name": "Other",
        "last_name": "Person",
        "gender": "M"
    }
    client.post(f"{BASE}/signup/", json=other_user_data)
    login_resp = client.post(f"{BASE}/login/", data={"username": "other_person", "password": "otherpass123"})
    other_token = login_resp.json()["access_token"]

    response = client.delete(f"{BASE}/posts/{post['id']}", headers=get_headers(other_token))
    assert response.status_code == 403


def test_delete_post_with_cover_image_calls_s3_delete(client, token):
    with patch("app.routes.posts.s3_utils.upload_image_to_s3", return_value="https://fake.s3.bucket.amazonaws.com/posts/img.jpg"), \
         patch("app.routes.posts.s3_utils.delete_s3_file") as mock_delete:
        fake_image = BytesIO(b"fakeimgcontent")
        post_response = client.post(
            f"{BASE}/posts/",
            data={"title": "Post com imagem", "content": "conteudo"},
            files={"cover_image": ("img.jpg", fake_image, "image/jpeg")},
            headers=get_headers(token)
        )
        assert post_response.status_code == 201
        post_id = post_response.json()["result"]["id"]

        delete_response = client.delete(f"{BASE}/posts/{post_id}", headers=get_headers(token))
        assert delete_response.status_code == 204
        mock_delete.assert_called_once()


# ---------------------------------------------------------------------------
# Create post with image
# ---------------------------------------------------------------------------

def test_create_post_with_image_uploads_to_s3(client, token):
    with patch("app.routes.posts.s3_utils.upload_image_to_s3", return_value="https://fake.s3.amazonaws.com/posts/img.jpg") as mock_upload:
        fake_image = BytesIO(b"imagedata")
        response = client.post(
            f"{BASE}/posts/",
            data={"title": "Post com foto", "content": "conteudo"},
            files={"cover_image": ("photo.jpg", fake_image, "image/jpeg")},
            headers=get_headers(token)
        )
        assert response.status_code == 201
        mock_upload.assert_called_once()


# ---------------------------------------------------------------------------
# Update error tests
# ---------------------------------------------------------------------------

def test_update_nonexistent_post_returns_404(client, token):
    response = client.put(
        f"{BASE}/posts/99999",
        data={"title": "New title"},
        files={},
        headers=get_headers(token)
    )
    assert response.status_code == 404


def test_update_post_only_title(client, token):
    post = create_post(client, token, title="Título inicial", content="Conteúdo fixo")

    response = client.put(
        f"{BASE}/posts/{post['id']}",
        data={"title": "Título alterado"},
        files={},
        headers=get_headers(token)
    )
    assert response.status_code == 200
    assert response.json()["result"]["title"] == "Título alterado"


def test_update_post_with_new_image(client, token):
    with patch("app.routes.posts.s3_utils.upload_image_to_s3", return_value="https://new.s3.amazonaws.com/posts/new.jpg") as mock_upload, \
         patch("app.routes.posts.s3_utils.delete_s3_file"):
        post = create_post(client, token, title="Post", content="content")

        fake_image = BytesIO(b"newimage")
        response = client.put(
            f"{BASE}/posts/{post['id']}",
            data={"title": "Updated with image"},
            files={"cover_image": ("new.jpg", fake_image, "image/jpeg")},
            headers=get_headers(token)
        )
        assert response.status_code == 200
        mock_upload.assert_called_once()


def test_delete_post_when_find_returns_none(client, token):
    """Covers posts.py:63 — dead-code guard after find_by_id returning None."""
    with patch("app.routes.posts.PostsRepo.find_by_id", return_value=None):
        response = client.delete(f"{BASE}/posts/1", headers=get_headers(token))
    assert response.status_code == 404


def test_get_post_when_find_returns_none(client, token):
    """Covers posts.py:90 — dead-code guard after find_by_id returning None."""
    with patch("app.routes.posts.PostsRepo.find_by_id", return_value=None):
        response = client.get(f"{BASE}/posts?post_id=1", headers=get_headers(token))
    assert response.status_code == 404


def test_update_post_when_find_returns_none(client, token):
    """Covers posts.py:119 — dead-code guard after find_by_id returning None."""
    with patch("app.routes.posts.PostsRepo.find_by_id", return_value=None):
        response = client.put(
            f"{BASE}/posts/1",
            data={"title": "x"},
            files={},
            headers=get_headers(token)
        )
    assert response.status_code == 404


def test_update_post_replaces_old_image_deletes_s3(client, token):
    """Covers posts.py:136 — old image deleted when new image uploaded."""
    with patch("app.routes.posts.s3_utils.upload_image_to_s3", return_value="https://fake.s3.amazonaws.com/posts/old.jpg"):
        fake_img = BytesIO(b"original")
        post_response = client.post(
            f"{BASE}/posts/",
            data={"title": "Post with image", "content": "content"},
            files={"cover_image": ("old.jpg", fake_img, "image/jpeg")},
            headers=get_headers(token)
        )
        assert post_response.status_code == 201
        post_id = post_response.json()["result"]["id"]

    with patch("app.routes.posts.s3_utils.upload_image_to_s3", return_value="https://fake.s3.amazonaws.com/posts/new.jpg") as mock_upload, \
         patch("app.routes.posts.s3_utils.delete_s3_file") as mock_delete:
        new_img = BytesIO(b"newcontent")
        response = client.put(
            f"{BASE}/posts/{post_id}",
            data={"title": "Updated"},
            files={"cover_image": ("new.jpg", new_img, "image/jpeg")},
            headers=get_headers(token)
        )
        assert response.status_code == 200
        mock_upload.assert_called_once()
        mock_delete.assert_called_once()
