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


def test_login_and_get_me():
    email = f"testuser_{uuid.uuid4()}@gmail.com"
    password = "password123"

    # 1. Create a user
    create_response = client.post(
        "/users/",
        json={
            "full_name": "Auth User",
            "email": email,
            "password": password
        }
    )
    assert create_response.status_code == 200

    # 2. Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"].lower() == "bearer"

    token = token_data["access_token"]

    # 3. Get current user
    me_response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == email
    assert me_data["full_name"] == "Auth User"


def test_update_profile():
    email = f"testuser_{uuid.uuid4()}@gmail.com"
    password = "password123"

    client.post("/users/", json={"full_name": "Update User", "email": email, "password": password})
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    update_response = client.put(
        "/users/me",
        headers=headers,
        json={"headline": "Test Headline", "location": "Test Location", "full_name": "New Name"}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["headline"] == "Test Headline"
    assert data["location"] == "Test Location"
    assert data["full_name"] == "New Name"

def test_change_password():
    email = f"testuser_{uuid.uuid4()}@gmail.com"
    password = "password123"
    new_password = "newpassword456"

    client.post("/users/", json={"full_name": "Pass User", "email": email, "password": password})
    login_response = client.post("/auth/login", json={"email": email, "password": password})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    change_pw_res = client.put(
        "/users/change-password",
        headers=headers,
        json={"old_password": password, "new_password": new_password}
    )
    assert change_pw_res.status_code == 200

    # Old login should fail
    login_old = client.post("/auth/login", json={"email": email, "password": password})
    assert login_old.status_code == 401
    
    # New login should succeed
    login_new = client.post("/auth/login", json={"email": email, "password": new_password})
    assert login_new.status_code == 200
