import io
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_resume_upload():
    email = f"resume_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "Resume User", "email": email, "password": "password123"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Standard PDF Upload
    file_content = b"Mock PDF Content"
    file = io.BytesIO(file_content)
    res = client.post("/resume/upload", headers=headers, files={"resume": ("resume.pdf", file, "application/pdf")})
    assert res.status_code == 200

    # Upload JPG should fail
    jpg_file = io.BytesIO(b"Mock JPG Content")
    res_jpg = client.post("/resume/upload", headers=headers, files={"resume": ("profile.jpg", jpg_file, "image/jpeg")})
    assert res_jpg.status_code == 400

    # Upload >10MB should fail
    large_file_content = b"0" * (11 * 1024 * 1024)
    large_file = io.BytesIO(large_file_content)
    res_large = client.post("/resume/upload", headers=headers, files={"resume": ("large.pdf", large_file, "application/pdf")})
    assert res_large.status_code == 400

    # Upload empty file
    empty_file = io.BytesIO(b"")
    res_empty = client.post("/resume/upload", headers=headers, files={"resume": ("empty.pdf", empty_file, "application/pdf")})
    assert res_empty.status_code == 400

def test_resume_download_and_delete():
    email = f"resume2_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "Resume User 2", "email": email, "password": "password123"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Upload first
    file = io.BytesIO(b"Downloadable Content")
    client.post("/resume/upload", headers=headers, files={"resume": ("resume2.pdf", file, "application/pdf")})

    # Download
    res_download = client.get("/resume/download", headers=headers)
    assert res_download.status_code == 200
    assert res_download.content == b"Downloadable Content"

    # Delete Resume
    res_delete = client.delete("/resume/", headers=headers)
    assert res_delete.status_code == 200

    # Delete Twice
    res_delete2 = client.delete("/resume/", headers=headers)
    assert res_delete2.status_code == 400 # Or 404 depending on how the route handles it. Wait, the route says "No resume uploaded" which is a 400. Let's assert 400.

    # Deleted resume download
    res_download2 = client.get("/resume/download", headers=headers)
    assert res_download2.status_code == 400 # The route raises 400 if it doesn't exist on user

def test_unauthorized_resume_ops():
    res = client.get("/resume/download")
    assert res.status_code == 401

    res2 = client.delete("/resume/")
    assert res2.status_code == 401
