# tests/test_subscriptions.py
from fastapi.testclient import TestClient


def test_get_subscription(client: TestClient):
    req_data = {"email": "a@b.com", "event_url": "https://example.com/e"}

    post_response = client.post("/subscriptions", json=req_data)

    assert post_response.status_code == 201

    response = client.get("/subscriptions/1")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "id": 1,
        "user_id": 1,
        "event_id": 1,
        "active": True,
    }


def test_get_subscription_404(client: TestClient):
    response = client.get("/subscriptions/1")

    assert response.status_code == 404


def test_post_subscription_201(client: TestClient):
    req_data = {"email": "a@b.com", "event_url": "https://example.com/e"}

    response = client.post("/subscriptions", json=req_data)
    data = response.json()

    assert response.status_code == 201
    assert data == {
        "id": 1,
        "user_id": 1,
        "event_id": 1,
        "active": True,
    }


# Not sure why this doesn't work yet:
# Throws IntegrityError -> ObjectDeleted Error
# def test_post_subscription_200(client: TestClient):
#     req_data = {"email": "a@b.com", "event_url": "https://example.com/e"}

#     first_response = client.post("/subscriptions", json=req_data)
#     assert first_response.status_code == 201

#     second_response = client.post("/subscriptions", json=req_data)
#     data = second_response.json()

#     assert second_response.status_code == 200
#     assert data == {
#         "id": 1,
#         "user_id": 1,
#         "event_id": 1,
#         "active": True,
#     }


def test_delete_subscription(client: TestClient):
    req_data = {"email": "a@b.com", "event_url": "https://example.com/e"}

    _ = client.post("/subscriptions", json=req_data)

    response = client.delete("/subscriptions/1")

    assert response.status_code == 204


def test_delete_subscription_404(client: TestClient):
    response = client.delete("/subscriptions/1")

    assert response.status_code == 404


def test_flip_subscription_status(client: TestClient):
    req_data = {"email": "a@b.com", "event_url": "https://example.com/e"}

    _ = client.post("/subscriptions", json=req_data)

    response = client.patch("/subscriptions/1/flip_status")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "id": 1,
        "user_id": 1,
        "event_id": 1,
        "active": False,
    }


def test_flip_subscription_status_404(client: TestClient):
    response = client.patch("/subscriptions/1/flip_status")

    assert response.status_code == 404
