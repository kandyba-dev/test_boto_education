from fastapi.testclient import TestClient
from src.database import init_db, get_connection
from src.main import app

client = TestClient(app)

def test_init_db_creates_table(tmp_path):
    init_db()
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='urls'"
        )
        table = cursor.fetchone()

    assert table is not None


def test_shorten_url():
    response = client.post("/shorten", params={"url": "https://example.com"})
    assert response.status_code == 200
    assert "short_url" in response.json()


def test_redirect_flow():
    shorten = client.post("/shorten", params={"url": "https://example.com"})
    short_url = shorten.json()["short_url"]
    code = short_url.split("/")[-1]

    redirect = client.get(f"/{code}", follow_redirects=False)
    assert redirect.status_code == 307


def test_invalid_url():
    response = client.post("/shorten", params={"url": "not-a-url"})
    assert response.status_code == 400


def test_custom_code_success():
    response = client.post(
        "/shorten", params={"url": "https://example.com", "custom_code": "my-code"}
    )
    assert response.status_code == 200
    assert response.json()["short_url"].endswith("/my-code")


def test_custom_code_conflict():
    client.post(
        "/shorten", params={"url": "https://example.com", "custom_code": "duplicate"}
    )

    response = client.post(
        "/shorten", params={"url": "https://example.com", "custom_code": "duplicate"}
    )

    assert response.status_code == 409
