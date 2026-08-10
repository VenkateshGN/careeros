import uuid
import io
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_headers():
    email = f"ai_tester_{uuid.uuid4()}@gmail.com"
    client.post("/users/", json={"full_name": "AI User", "email": email, "password": "password123"})
    token = client.post("/auth/login", json={"email": email, "password": "password123"}).json()["access_token"]
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

def test_resume_review_grammar_and_missing():
    headers = get_auth_headers()
    with patch("app.services.ai_service.generate_resume_review") as mock_generate:
        mock_generate.return_value = {
            "overall_score": 60,
            "strengths": [],
            "weaknesses": ["Grammar mistakes", "Missing keywords like Python"],
            "suggestions": ["Fix typos", "Add Python to skills"]
        }
        res = client.post("/ai/resume-review", json={"resume_url": "mock_url2.pdf"}, headers=headers)
    assert res.status_code == 200
    assert "Grammar mistakes" in res.json()["weaknesses"]

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

def test_job_matching():
    headers = get_auth_headers()
    response = client.post(
        "/ai/job-matching",
        json={"resume_text": "I know Python and React", "job_description": "We need Python and Rust"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "match_score" in data
    assert "missing_skills" in data

def test_ai_resume_parser_conditions():
    headers = get_auth_headers()

    # Skills extracted
    with patch("app.services.ai_service.extract_structured_resume_data") as mock_extract:
        mock_extract.return_value = {"skills": ["Python", "FastAPI"], "projects": ["Project A"]}
        file = io.BytesIO(b"Resume content with skills")
        res = client.post("/resume/upload", headers=headers, files={"resume": ("resume.pdf", file, "application/pdf")})
        assert "Python" in res.json()["structured_data"]["skills"]

        # Verify database save
        me_res = client.get("/users/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["skills"] == "Python, FastAPI"

    # Without skills
    with patch("app.services.ai_service.extract_structured_resume_data") as mock_extract:
        mock_extract.return_value = {"skills": [], "projects": ["Project A"]}
        file = io.BytesIO(b"Resume content no skills")
        res2 = client.post("/resume/upload", headers=headers, files={"resume": ("resume.pdf", file, "application/pdf")})
        assert len(res2.json()["structured_data"]["skills"]) == 0

    # Blank PDF (No data)
    with patch("app.services.ai_service.extract_structured_resume_data") as mock_extract:
        mock_extract.return_value = {}
        file = io.BytesIO(b"Blank PDF")
        res3 = client.post("/resume/upload", headers=headers, files={"resume": ("resume.pdf", file, "application/pdf")})
        # Depends on implementation, might return empty structured data
        assert ("structured_data" in res3.json())

def test_bedrock_unavailable():
    headers = get_auth_headers()
    # Test fallback gracefully by mocking bedrock client to raise Exception
    with patch("app.services.ai_service.bedrock_client") as mock_bedrock_client:
        mock_bedrock_client.invoke_model.side_effect = Exception("AWS Bedrock temporarily down")
        response = client.post("/ai/job-matching", json={"resume_text": "a", "job_description": "b"}, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["match_score"] == 86
        assert "Python" in data["matched_skills"]

# --- AI Career Assistant - Functional Test Cases (AI-01 to AI-06) ---

def test_ai_career_assistant_basic_and_senior():
    headers = get_auth_headers()

    # AI-01: Basic career question
    response = client.post(
        "/ai/agent/chat",
        json={"message": "I want to get an SDE job. What skills do I need?"},
        headers=headers
    )
    assert response.status_code == 200
    assert "reply" in response.json()

    # AI-02: Senior role question
    response = client.post(
        "/ai/agent/chat",
        json={"message": "What skills do I need for Senior Software Engineer?"},
        headers=headers
    )
    assert response.status_code == 200
    assert "reply" in response.json()

def test_ai_career_assistant_edge_cases():
    headers = get_auth_headers()

    # AI-03: Empty question
    response = client.post("/ai/agent/chat", json={"message": ""}, headers=headers)
    assert response.status_code in [200, 422]

    # AI-04: Very long question
    long_msg = "SDE question " * 500
    response = client.post("/ai/agent/chat", json={"message": long_msg}, headers=headers)
    assert response.status_code == 200
    assert "reply" in response.json()

def test_ai_career_assistant_general_and_comparison():
    headers = get_auth_headers()

    # AI-05: General career question
    response = client.post("/ai/agent/chat", json={"message": "How can I improve my career?"}, headers=headers)
    assert response.status_code == 200

    # AI-06: Technical question comparison
    response = client.post("/ai/agent/chat", json={"message": "Should I learn Java or Python for SDE?"}, headers=headers)
    assert response.status_code == 200


# --- AWS Bedrock Connection Tests (AWS-01 to AWS-08) & Fallbacks ---

@patch("app.services.ai_service.bedrock_client")
def test_aws_bedrock_connections(mock_bedrock_client):
    headers = get_auth_headers()
    from botocore.exceptions import ClientError
    import io

    # Mock successful call (AWS-01 / AWS-07)
    class MockStreamingBody:
        def read(self):
            return b'{"content": [{"text": "{\\"reply\\": \\"Mocked response\\"}"}]}'

    mock_response = {
        "body": MockStreamingBody()
    }
    mock_bedrock_client.invoke_model.return_value = mock_response

    response = client.post("/ai/agent/chat", json={"message": "Hello"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["reply"] == "Mocked response"

    # AWS-02 / AWS-03: Invalid credentials / secret key
    mock_bedrock_client.invoke_model.side_effect = ClientError(
        {"Error": {"Code": "UnrecognizedClientException", "Message": "The security token included in the request is invalid"}},
        "invoke_model"
    )
    response = client.post("/ai/agent/chat", json={"message": "Hello"}, headers=headers)
    assert response.status_code == 200
    assert "technical difficulties" in response.json()["reply"].lower() or "please try again" in response.json()["reply"].lower()

    # AWS-04: Invalid region
    from botocore.exceptions import EndpointConnectionError
    mock_bedrock_client.invoke_model.side_effect = EndpointConnectionError(endpoint_url="https://bedrock.us-east-100.amazonaws.com")
    response = client.post("/ai/agent/chat", json={"message": "Hello"}, headers=headers)
    assert response.status_code == 200

    # AWS-05: Model unavailable
    mock_bedrock_client.invoke_model.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "The model requested is not available"}},
        "invoke_model"
    )
    response = client.post("/ai/agent/chat", json={"message": "Hello"}, headers=headers)
    assert response.status_code == 200

    # AWS-06: Bedrock service temporarily unavailable
    mock_bedrock_client.invoke_model.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "Internal server error occurred"}},
        "invoke_model"
    )
    response = client.post("/ai/agent/chat", json={"message": "Hello"}, headers=headers)
    assert response.status_code == 200

    # AWS-08: Timeout
    from botocore.exceptions import ReadTimeoutError
    mock_bedrock_client.invoke_model.side_effect = ReadTimeoutError(endpoint_url="bedrock", request={})
    response = client.post("/ai/agent/chat", json={"message": "Hello"}, headers=headers)
    assert response.status_code == 200
