import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_user_analytics():
    email = f"dashboard_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "Dash User", "email": email, "password": "password123"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Check dashboard without resume
    res = client.get("/dashboard/user-analytics", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["analytics"]["resume_score"] == 0
    assert data["analytics"]["applications_submitted"] == 0

    # After uploading a resume, the score should change
    import io
    file = io.BytesIO(b"Dash PDF")
    client.post("/resume/upload", headers=headers, files={"resume": ("dash.pdf", file, "application/pdf")})

    res2 = client.get("/dashboard/user-analytics", headers=headers)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["analytics"]["resume_score"] == 40
