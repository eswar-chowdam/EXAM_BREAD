from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_user_registration_and_login_flow():
    register_response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Alice Student",
            "email": "alice@example.com",
            "password": "StrongPass123!",
        },
    )

    assert register_response.status_code == 201
    register_payload = register_response.json()
    assert register_payload["user"]["email"] == "alice@example.com"
    assert register_payload["token"]

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "alice@example.com",
            "password": "StrongPass123!",
        },
    )

    assert login_response.status_code == 200
    login_payload = login_response.json()
    assert login_payload["token"]

    me_response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {login_payload['token']}"},
    )

    assert me_response.status_code == 200
    assert me_response.json()["email"] == "alice@example.com"
