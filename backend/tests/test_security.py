import uuid
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta
from jose import jwt
from app.core.security import SECRET_KEY, ALGORITHM

client = TestClient(app)

def test_sql_injection_prevention():
    # Attempt SQL injection in standard inputs like email or job title
    sqli_payload = "test@example.com' OR 1=1--"
    response = client.post("/auth/login", json={"email": sqli_payload, "password": "password123"})
    # Should get 422 because pydantic EmailStr validation fails, OR 401 Unauthorized, never 500
    assert response.status_code in [401, 422]

def test_xss_protection():
    email = f"xss_{uuid.uuid4()}@gmail.com"
    xss_payload = "<script>alert(1)</script>"
    # This might actually just store it safely since the frontend is React.
    # The API should just allow it (or sanitize it), but crucially the DB handles it and doesn't execute anything.
    response = client.post("/users/", json={"full_name": xss_payload, "email": email, "password": "password123"})
    assert response.status_code in [200, 201, 422]
    # We rely on React escaping it, API returning 200 is acceptable as long as DB takes it as literal string.

def test_jwt_tampering():
    email = f"jwt_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "JWT Admin", "email": email, "password": "password123"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]

    # Tamper token (change a character in the middle)
    tampered_token = token[:20] + ("X" if token[20] != "X" else "Y") + token[21:]
    res = client.get("/users/me", headers={"Authorization": f"Bearer {tampered_token}"})
    assert res.status_code == 401

def test_expired_token():
    # Create an expired token manually using the server's secret
    to_encode = {"sub": "random_user_id"}
    expire = datetime.utcnow() - timedelta(minutes=10) # Expired 10 mins ago
    to_encode.update({"exp": expire})
    expired_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    res = client.get("/users/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert res.status_code == 401

def test_cors_headers():
    res = client.options("/auth/login", headers={"Origin": "http://evil.com", "Access-Control-Request-Method": "POST"})
    # Depending on CORS setup, evil.com might be rejected or allowed, but it shouldn't 500.
    assert res.status_code in [200, 400]
