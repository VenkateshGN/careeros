import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_recruiter_headers():
    email = f"recruiter_app_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "Recruiter App", "email": email, "password": "password123", "role": "recruiter"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_apply_for_job():
    import io
    email = f"app_tester_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "App User", "email": email, "password": "password123"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Needs a real user with a role allowed to post jobs if job auth is enforced
    recruiter_headers = get_recruiter_headers()
    job_res = client.post("/jobs/", headers=recruiter_headers, json={"title": "Dev", "description": "D", "company": "C", "location": "Remote", "salary_min": 1, "salary_max": 2})
    job_id = job_res.json()["id"]

    # Without resume, should fail
    apply_fail = client.post(f"/jobs/{job_id}/apply", headers=headers, json={"cover_letter_text": ""})
    assert apply_fail.status_code == 400
    assert "upload a resume" in apply_fail.json()["detail"].lower()

    # Upload resume
    file = io.BytesIO(b"Mock PDF Content")
    client.post("/resume/upload", headers=headers, files={"resume": ("resume.pdf", file, "application/pdf")})

    # Apply
    apply_success = client.post(f"/jobs/{job_id}/apply", headers=headers, json={"cover_letter_text": ""})
    assert apply_success.status_code == 201

    # Second apply fail (duplicate)
    apply_dup = client.post(f"/jobs/{job_id}/apply", headers=headers, json={"cover_letter_text": ""})
    assert apply_dup.status_code == 400
    assert "already applied" in apply_dup.json()["detail"].lower()

    # Invalid job id (UUID format check)
    apply_invalid = client.post(f"/jobs/00000000-0000-0000-0000-000000000000/apply", headers=headers, json={"cover_letter_text": ""})
    assert apply_invalid.status_code == 404

def test_withdraw_application():
    import io
    email = f"app_with_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "App User", "email": email, "password": "password123"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Job
    recruiter_headers = get_recruiter_headers()
    job_res = client.post("/jobs/", headers=recruiter_headers, json={"title": "Dev 2", "description": "D2", "company": "C", "location": "Remote"})
    job_id = job_res.json()["id"]

    # Resume & Apply
    file = io.BytesIO(b"Mock PDF")
    client.post("/resume/upload", headers=headers, files={"resume": ("res.pdf", file, "application/pdf")})
    apply_res = client.post(f"/jobs/{job_id}/apply", headers=headers, json={"cover_letter_text": ""})
    app_id = apply_res.json()["id"]

    # Withdraw
    with_res = client.delete(f"/applications/{app_id}", headers=headers)
    assert with_res.status_code == 204

    # Withdraw again -> Error (404)
    with_res2 = client.delete(f"/applications/{app_id}", headers=headers)
    assert with_res2.status_code == 404
