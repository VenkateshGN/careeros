import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_apply_for_job():
    # Need a user with resume and a job
    email = f"applicant_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "App User", "email": email, "password": "pwd"})
    token = client.post("/auth/login", json={"email": email, "password": "pwd"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Without resume, should fail
    job_res = client.post("/jobs/", json={"title": "Dev", "description": "D", "company": "C"})
    job_id = job_res.json()["id"]
    
    apply_fail = client.post(f"/jobs/{job_id}/apply", headers=headers, json={})
    assert apply_fail.status_code == 400
    assert "upload a resume" in apply_fail.json()["detail"]
    
    # After resume upload:
    import io
    file_content = b"Mock PDF Content"
    file = io.BytesIO(file_content)
    file.name = "resume.pdf"
    
    client.post(
        "/resume/upload",
        headers=headers,
        files={"resume": ("resume.pdf", file, "application/pdf")}
    )
    
    apply_success = client.post(f"/jobs/{job_id}/apply", headers=headers, json={})
    assert apply_success.status_code == 201
    
    # Second apply fail
    apply_dup = client.post(f"/jobs/{job_id}/apply", headers=headers, json={})
    assert apply_dup.status_code == 400
    assert "Already applied" in apply_dup.json()["detail"]
