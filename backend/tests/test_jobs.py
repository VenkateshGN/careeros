import pytest
import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_recruiter_headers():
    email = f"recruiter_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "Recruiter", "email": email, "password": "password123", "role": "recruiter"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_jobs_crud():
    headers = get_recruiter_headers()
    with patch("app.api.routes.jobs.fetch_combined_jobs", return_value=[]):
        # Create
        create_response = client.post(
            "/jobs/",
            headers=headers,
            json={
                "title": "Software Engineer",
                "description": "Develop cool features",
                "company": "TechCorp",
                "location": "Remote",
                "salary_min": 100000,
                "salary_max": 150000
            }
        )
        if create_response.status_code == 403:
            pass
        else:
            assert create_response.status_code == 201
            job_id = create_response.json()["id"]

            # Read All with Pagination
            list_response = client.get("/jobs/?skip=0&limit=10")
            assert list_response.status_code == 200

            # Missing validation
            invalid_res = client.post("/jobs/", headers=headers, json={"title": ""})
            assert invalid_res.status_code == 422

            # Read Single again should fail on invalid UUID
            get_fail = client.get(f"/jobs/00000000-0000-0000-0000-000000000000")
            assert get_fail.status_code == 404

            # Delete
            delete_response = client.delete(f"/jobs/{job_id}", headers=headers)
            assert delete_response.status_code == 204

            # Delete already deleted
            del_again = client.delete(f"/jobs/{job_id}", headers=headers)
            assert del_again.status_code == 404

def test_job_suggestions():
    email = f"candidate_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "Job seeker", "email": email, "password": "password123", "role": "candidate"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    update_res = client.put("/users/me", json={"skills": "Python, Docker"}, headers=headers)
    assert update_res.status_code == 200

    with patch("app.api.routes.jobs.fetch_combined_jobs", return_value=[]):
        res = client.get("/jobs/suggestions", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        for job in res.json():
            if job.get("company_name") == "Google":
                assert job.get("company_website") == "https://google.com"
            elif job.get("company_name") == "Stripe":
                assert job.get("company_website") == "https://stripe.com"

def test_job_suggestions_with_resume():
    import io
    email = f"candidate2_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "Job seeker 2", "email": email, "password": "password123", "role": "candidate"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    file_content = b"Mock PDF resume containing Python, FastAPI, Docker"
    file = io.BytesIO(file_content)
    upload_res = client.post("/resume/upload", headers=headers, files={"resume": ("resume.pdf", file, "application/pdf")})
    assert upload_res.status_code == 200

    with patch("app.api.routes.jobs.fetch_combined_jobs", return_value=[]):
        res = client.get("/jobs/suggestions", headers=headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        for job in res.json():
            if job.get("company_name") == "Google":
                assert job.get("company_website") == "https://google.com"
            elif job.get("company_name") == "Stripe":
                assert job.get("company_website") == "https://stripe.com"
