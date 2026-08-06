import io
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_resume_upload():
    email = f"resume_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "Resume User", "email": email, "password": "pwd"})
    token = client.post("/auth/login", json={"email": email, "password": "pwd"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    file_content = b"Mock PDF Content"
    file = io.BytesIO(file_content)
    file.name = "resume.pdf"
    
    res = client.post(
        "/resume/upload",
        headers=headers,
        files={"resume": ("resume.pdf", file, "application/pdf")}
    )
    
    assert res.status_code == 200
    data = res.json()
    assert "resume_url" in data
    assert "uploads/resumes" in data["resume_url"]
