import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_jobs_crud():
    # Create
    create_response = client.post(
        "/jobs/",
        json={
            "title": "Software Engineer",
            "description": "Develop cool features",
            "company": "TechCorp",
            "location": "Remote",
            "salary_min": 100000,
            "salary_max": 150000
        }
    )
    assert create_response.status_code == 201
    job_id = create_response.json()["id"]

    # Read All
    list_response = client.get("/jobs/")
    assert list_response.status_code == 200
    assert len(list_response.json()) > 0

    # Read Single
    get_response = client.get(f"/jobs/{job_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Software Engineer"
    
    # Update
    update_response = client.put(
        f"/jobs/{job_id}",
        json={"title": "Senior Software Engineer"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Senior Software Engineer"
    
    # Delete
    delete_response = client.delete(f"/jobs/{job_id}")
    assert delete_response.status_code == 204
    
    # Read Single again should fail
    get_response_2 = client.get(f"/jobs/{job_id}")
    assert get_response_2.status_code == 404
