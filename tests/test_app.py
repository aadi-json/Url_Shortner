import pytest

from app import create_app, db
from app.models import Link, User
from app.utils import create_link, is_valid_url


@pytest.fixture
def app():
    app = create_app("config.TestConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def signup(client, email="a@example.com", password="password123"):
    return client.post("/signup", data={"email": email, "password": password},
                       follow_redirects=True)


def test_signup_logs_in_and_hashes_password(client):
    resp = signup(client)
    assert resp.status_code == 200
    user = User.query.filter_by(email="a@example.com").first()
    assert user is not None
    assert user.password_hash != "password123"


def test_duplicate_email_rejected(client):
    signup(client)
    client.post("/logout")
    resp = signup(client)
    assert b"already exists" in resp.data
    assert User.query.count() == 1


def test_login_wrong_password(client):
    signup(client)
    client.post("/logout")
    resp = client.post("/login", data={"email": "a@example.com", "password": "wrongpass"})
    assert b"Invalid email or password" in resp.data


def test_dashboard_requires_login(client):
    resp = client.get("/dashboard")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_create_link_and_redirect_counts_clicks(client):
    signup(client)
    client.post("/dashboard", data={"url": "https://example.com/page"})
    link = Link.query.one()
    assert len(link.short_code) == 6
    for _ in range(3):
        resp = client.get(f"/{link.short_code}")
        assert resp.status_code == 302
        assert resp.headers["Location"] == "https://example.com/page"
    db.session.refresh(link)
    assert link.clicks == 3


def test_invalid_url_rejected(client):
    signup(client)
    client.post("/dashboard", data={"url": "javascript:alert(1)"})
    assert Link.query.count() == 0


def test_user_cannot_delete_others_link(app, client):
    signup(client, "a@example.com")
    client.post("/dashboard", data={"url": "https://example.com"})
    link_id = Link.query.one().id
    client.post("/logout")
    signup(client, "b@example.com")
    resp = client.post(f"/links/{link_id}/delete")
    assert resp.status_code == 404
    assert Link.query.count() == 1


def test_pagination(app, client):
    signup(client)
    user = User.query.one()
    for i in range(12):
        create_link(f"https://example.com/{i}", user)
    page1 = client.get("/dashboard")
    page2 = client.get("/dashboard?page=2")
    assert b"Page 1 of 2" in page1.data
    assert b"Page 2 of 2" in page2.data


def test_unknown_code_404(client):
    assert client.get("/nope123").status_code == 404


def test_is_valid_url():
    assert is_valid_url("https://example.com")
    assert not is_valid_url("example.com")
    assert not is_valid_url("ftp://example.com")
