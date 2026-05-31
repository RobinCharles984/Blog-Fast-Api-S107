import pytest
from fastapi import HTTPException

from app.models.posts import Posts
from app.models.users import Users
from app.repositories.posts_repo import PostsRepo
from app.repositories.user_repo import UserRepo


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_user_obj(
    username="repo_user",
    email="repo@example.com",
    phone="35900000001",
    role="user"
):
    return Users(
        username=username,
        email=email,
        password="hashedpass",
        phone_number=phone,
        first_name="Repo",
        last_name="Test",
        gender="male",
        role=role,
    )


def make_post_obj(author_id, title="Repo Post", content="Conteúdo"):
    return Posts(title=title, author_id=author_id, content=content)


# ---------------------------------------------------------------------------
# UserRepo tests
# ---------------------------------------------------------------------------

class TestUserRepo:
    def test_insert_creates_user_with_id(self, session):
        user = make_user_obj()
        UserRepo.insert(session, user)
        assert user.id is not None

    def test_find_by_username_found(self, session):
        user = make_user_obj()
        UserRepo.insert(session, user)
        found = UserRepo.find_by_username(session, "repo_user")
        assert found is not None
        assert found.username == "repo_user"

    def test_find_by_username_not_found(self, session):
        result = UserRepo.find_by_username(session, "nonexistent")
        assert result is None

    def test_find_by_email_found(self, session):
        user = make_user_obj()
        UserRepo.insert(session, user)
        found = UserRepo.find_by_email(session, "repo@example.com")
        assert found is not None
        assert found.email == "repo@example.com"

    def test_find_by_email_not_found(self, session):
        result = UserRepo.find_by_email(session, "nobody@example.com")
        assert result is None

    def test_find_by_id_found(self, session):
        user = make_user_obj()
        UserRepo.insert(session, user)
        found = UserRepo.find_by_id(session, user.id)
        assert found.id == user.id

    def test_find_by_id_not_found_raises_404(self, session):
        with pytest.raises(HTTPException) as exc_info:
            UserRepo.find_by_id(session, 99999)
        assert exc_info.value.status_code == 404

    def test_promote_sets_role_to_admin(self, session):
        user = make_user_obj()
        UserRepo.insert(session, user)
        assert user.role == "user"
        promoted = UserRepo.promote(session, user)
        assert promoted.role == "admin"


# ---------------------------------------------------------------------------
# PostsRepo tests
# ---------------------------------------------------------------------------

class TestPostsRepo:
    def _create_author(self, session):
        user = make_user_obj(username="author", email="author@example.com", phone="35900000099")
        UserRepo.insert(session, user)
        return user

    def test_insert_creates_post_with_id(self, session):
        author = self._create_author(session)
        post = make_post_obj(author_id=author.id)
        PostsRepo.insert(session, post)
        assert post.id is not None

    def test_delete_removes_post(self, session):
        author = self._create_author(session)
        post = make_post_obj(author_id=author.id)
        PostsRepo.insert(session, post)
        post_id = post.id
        PostsRepo.delete(session, post)
        with pytest.raises(HTTPException):
            PostsRepo.find_by_id(session, post_id)

    def test_find_all_returns_list(self, session):
        author = self._create_author(session)
        PostsRepo.insert(session, make_post_obj(author_id=author.id, title="P1"))
        PostsRepo.insert(session, make_post_obj(author_id=author.id, title="P2"))
        all_posts = PostsRepo.find_all(session)
        assert len(all_posts) >= 2

    def test_find_all_paginated_respects_limit(self, session):
        author = self._create_author(session)
        for i in range(5):
            PostsRepo.insert(session, make_post_obj(author_id=author.id, title=f"Post {i}"))
        page = PostsRepo.find_all_paginated(session, skip=0, limit=3)
        assert len(page) == 3

    def test_find_all_paginated_respects_skip(self, session):
        author = self._create_author(session)
        for i in range(4):
            PostsRepo.insert(session, make_post_obj(author_id=author.id, title=f"Skip {i}"))
        all_posts = PostsRepo.find_all_paginated(session, skip=0, limit=10)
        skipped = PostsRepo.find_all_paginated(session, skip=2, limit=10)
        assert len(skipped) == len(all_posts) - 2

    def test_find_by_id_found(self, session):
        author = self._create_author(session)
        post = make_post_obj(author_id=author.id)
        PostsRepo.insert(session, post)
        found = PostsRepo.find_by_id(session, post.id)
        assert found.id == post.id

    def test_find_by_id_not_found_raises_404(self, session):
        with pytest.raises(HTTPException) as exc_info:
            PostsRepo.find_by_id(session, 99999)
        assert exc_info.value.status_code == 404

    def test_update_title_only(self, session):
        author = self._create_author(session)
        post = make_post_obj(author_id=author.id, title="Original", content="Conteúdo original")
        PostsRepo.insert(session, post)
        updated = PostsRepo.update(session, post, title="Novo Título")
        assert updated.title == "Novo Título"
        assert updated.content == "Conteúdo original"

    def test_update_content_only(self, session):
        author = self._create_author(session)
        post = make_post_obj(author_id=author.id, title="Título fixo", content="Antigo conteúdo")
        PostsRepo.insert(session, post)
        updated = PostsRepo.update(session, post, content="Novo conteúdo")
        assert updated.title == "Título fixo"
        assert updated.content == "Novo conteúdo"

    def test_update_all_fields(self, session):
        author = self._create_author(session)
        post = make_post_obj(author_id=author.id, title="Antes", content="Antes")
        PostsRepo.insert(session, post)
        updated = PostsRepo.update(
            session, post,
            title="Depois",
            content="Novo conteúdo",
            cover_image_url="https://img.url/new.jpg",
            author_id=author.id
        )
        assert updated.title == "Depois"
        assert updated.content == "Novo conteúdo"
        assert updated.cover_image_url == "https://img.url/new.jpg"
