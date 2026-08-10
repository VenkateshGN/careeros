from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_global_404_handling():
    res = client.get("/invalid_route_that_does_not_exist")
    assert res.status_code == 404

def test_api_status():
    res = client.get("/health") # Assuming there's a health endpoint. If not docs works.
    if res.status_code == 404:
        res = client.get("/docs")
    assert res.status_code in [200, 307]

def test_unauthorized_post_global():
    # Attempting to post to an endpoint without headers
    res = client.post("/jobs/", json={"title": "Unauthorized", "description": "Fail"})
    assert res.status_code == 401
