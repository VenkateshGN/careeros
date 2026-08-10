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

def test_update_profile_links_and_empty():
    email = f"profile_link_{uuid.uuid4()}@gmail.com"
    password = "password123"
    client.post("/users/", json={"full_name": "Link User", "email": email, "password": password})
    token = client.post("/auth/login", json={"email": email, "password": password}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Update skills, github, linkedin
    res = client.put("/users/me", headers=headers, json={"skills": "Python, React", "github_url": "https://github.com/user", "linkedin_url": "https://linkedin.com/in/user"})
    assert res.status_code == 200
    data = res.json()
    assert data["skills"] == "Python, React"
    # Note Pydantic v2 returns URLs as string representations when dumped, but the API may return it directly stringified.
    assert "github.com/user" in str(data["github_url"])

    # Empty request -> Should not change anything
    res_empty = client.put("/users/me", headers=headers, json={})
    assert res_empty.status_code == 200
    data_empty = res_empty.json()
    assert data_empty["full_name"] == "Link User"  # Still the same

    # Invalid URL
    res_invalid = client.put("/users/me", headers=headers, json={"github_url": "not-a-url"})
    assert res_invalid.status_code == 422


def test_get_deleted_user_unauthorized():
    res = client.get("/users/me")
    assert res.status_code == 401

def test_unauthorized_request():
    res = client.put("/users/me", json={"full_name": "Unauthorized"})
    assert res.status_code == 401

def test_invalid_token():
    headers = {"Authorization": "Bearer invalid.token.here"}
    res = client.put("/users/me", headers=headers, json={"full_name": "Invalid Token Test"})
    assert res.status_code == 401
