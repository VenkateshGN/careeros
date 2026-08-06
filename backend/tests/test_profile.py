import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_update_profile_full_name_bio_location():
    email = f"profile_{uuid.uuid4()}@gmail.com"
    password = "password123"

    # Register and Login
    client.post("/users/", json={"full_name": "Initial Name", "email": email, "password": password})
    token = client.post("/auth/login", json={"email": email, "password": password}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Update profile
    update_data = {
        "full_name": "Updated Name",
        "bio": "Software engineer with 5 years experience.",
        "location": "Bengaluru"
    }

    res = client.put("/users/me", headers=headers, json=update_data)
    assert res.status_code == 200
    
    data = res.json()
    assert data["full_name"] == "Updated Name"
    assert data["bio"] == "Software engineer with 5 years experience."
    assert data["location"] == "Bengaluru"

def test_unauthorized_request():
    res = client.put("/users/me", json={"full_name": "Unauthorized"})
    assert res.status_code == 401

def test_invalid_token():
    headers = {"Authorization": "Bearer invalid.token.here"}
    res = client.put("/users/me", headers=headers, json={"full_name": "Invalid Token Test"})
    assert res.status_code == 401
