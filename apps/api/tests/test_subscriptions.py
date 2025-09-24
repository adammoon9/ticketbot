# tests/test_subscriptions.py
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_and_get():
    r = client.post("/subscriptions", json={"email":"a@b.com","event_url":"https://example.com/e"})
    assert r.status_code == 201
    sub = r.json()
    r2 = client.get(f"/subscriptions/{sub['id']}")
    assert r2.status_code == 200
