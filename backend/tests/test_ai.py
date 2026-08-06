import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers():
    email = f"ai_tester_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "AI User", "email": email, "password": "pwd"})
    token = client.post("/auth/login", json={"email": email, "password": "pwd"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_resume_review():
    headers = get_auth_headers()
    response = client.post(
        "/ai/resume-review",
        json={"resume_url": "mock_url.pdf"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert len(data["strengths"]) > 0

def test_career_roadmap():
    headers = get_auth_headers()
    response = client.post(
        "/ai/career-roadmap",
        json={"current_role": "Junior Dev", "target_role": "Senior Dev"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["steps"]) > 0
    assert data["target_role"] == "Senior Dev"

def test_mock_interview():
    headers = get_auth_headers()
    response = client.post(
        "/ai/mock-interview-questions",
        json={"job_title": "Frontend Engineer"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["questions"]) > 0
    assert data["job_title"] == "Frontend Engineer"
