import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_user():

    email = f"testuser_{uuid.uuid4()}@gmail.com"

    response = client.post(
        "/users/",
        json={
            "full_name": "Test User",
            "email": email,
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == "Test User"
    assert data["email"] == email

    # Security checks
    assert "password" not in data
    assert "password_hash" not in data