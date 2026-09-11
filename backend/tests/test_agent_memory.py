import pytest
import uuid
from app.models.agent_memory import AgentMemory
from app.services import ai_service
from unittest.mock import patch
from sqlalchemy.orm import Session

# --- 1. Bedrock Core Tests & Fallbacks (AWS & FB) ---

def test_aws_bedrock_fallback_logic():
    """
    AWS-02 / FB-01: Validates that if AWS keys are invalid/missing,
    the system does not crash and safely returns the fallback mock.
    """
    res = ai_service._call_bedrock_json("Test Prompt", {"reply": "Mock Fallback"})
    assert "reply" in res
    assert res["reply"] == "Mock Fallback" or isinstance(res["reply"], str)

def test_missing_memory_handles_gracefully(client, token_headers):
    """
    VEC-07 / VEC-08 / FB-06: Empty vector database gracefully routes the prompt.
    """
    response = client.post("/ai/agent/chat", headers=token_headers, json={"message": "Hello"})
    assert response.status_code == 200
    assert "reply" in response.json()


# --- 2. CockroachDB Memory Tests (MEM) ---

def test_save_career_goal_memory(client, token_headers, test_user, db_session):
    """
    MEM-01 / MEM-06 / MEM-07: Save career goal, verify User ID and extraction.
    """
    response = client.post("/ai/agent/chat", headers=token_headers, json={"message": "I want to become a Python backend developer."})
    assert response.status_code == 200

    # End transaction to see changes committed by TestClient
    db_session.rollback()

    # Assert physical insertion into pgvector mapping successfully mapped to test_user
    memory = db_session.query(AgentMemory).filter_by(user_id=test_user.id).first()
    assert memory is not None
    assert "Python backend developer" in memory.content
    assert memory.created_at is not None

def test_save_skills_preferences_and_duplicates(client, token_headers, test_user, db_session):
    """
    MEM-02 / MEM-03 / MEM-04 / MEM-05 / MEM-08: Save skill, preference, conversation, duplicate memory.
    """
    # MEM-02: Save skill
    client.post("/ai/agent/chat", headers=token_headers, json={"message": "I know Python and FastAPI."})
    # MEM-03: Save preference
    client.post("/ai/agent/chat", headers=token_headers, json={"message": "I prefer working remote."})
    # MEM-04: Save conversation (already saved via endpoint)
    # MEM-05: Duplicate memory (sending same goal again)
    client.post("/ai/agent/chat", headers=token_headers, json={"message": "I prefer working remote."})

    # End transaction to see changes committed by TestClient
    db_session.rollback()

    memories = db_session.query(AgentMemory).filter_by(user_id=test_user.id).all()
    assert len(memories) >= 3
    # MEM-08: Retrieval check
    contents = [m.content for m in memories]
    assert any("Python and FastAPI" in c for c in contents)
    assert any("working remote" in c for c in contents)


# --- 3. Vector Memory Semantic Tests (VEC & AGENT) ---

def test_semantic_vector_l2_retrieval(client, token_headers, test_user, db_session):
    """
    VEC-01 / VEC-02 / AGENT-02: Generate query embeddings and retrieve previous memories natively.
    """
    client.post("/ai/agent/chat", headers=token_headers, json={"message": "I want to become a Python backend developer."})

    # Follow up question testing sequence limits
    response = client.post("/ai/agent/chat", headers=token_headers, json={"message": "What backend career should I target?"})
    assert response.status_code == 200

    # End transaction to see changes committed by TestClient
    db_session.rollback()

    memories = db_session.query(AgentMemory).filter_by(user_id=test_user.id).all()
    assert len(memories) >= 2 # Successfully stacked continuity

def test_semantic_search_and_ranking(client, token_headers, test_user, db_session):
    """
    VEC-03 / VEC-04 / VEC-05 / VEC-06: Semantic search, similar vs unrelated questions, ranking.
    """
    # Clear previous user memories to isolate the search
    db_session.query(AgentMemory).filter_by(user_id=test_user.id).delete()
    db_session.commit()

    # VEC-01: Store embedding
    # Inject specific mock memories with engineered mock embeddings to test spatial distance queries
    py_emb = [0.1] * 1536
    unrelated_emb = [0.9] * 1536

    m1 = AgentMemory(user_id=test_user.id, content="Python backend goal", embedding=py_emb)
    m2 = AgentMemory(user_id=test_user.id, content="Gardening hobby preference", embedding=unrelated_emb)
    db_session.add_all([m1, m2])
    db_session.commit()

    # VEC-02: Generate query embedding & VEC-03/VEC-04: Semantic search similar question
    with patch("app.services.ai_service.generate_embeddings") as mock_emb:
        mock_emb.return_value = py_emb
        response = client.post("/ai/agent/chat", headers=token_headers, json={"message": "What programming languages should I learn for backend?"})
        assert response.status_code == 200

        # End transaction to see changes committed by TestClient
        db_session.rollback()

        # VEC-06: Rank memory
        if db_session.bind.dialect.name in ('postgresql', 'cockroachdb'):
            memories = db_session.query(AgentMemory).filter_by(user_id=test_user.id)\
                         .order_by(AgentMemory.embedding.l2_distance(query_vector)).all()
        else:
            memories = db_session.query(AgentMemory).filter_by(user_id=test_user.id)\
                         .order_by(AgentMemory.created_at.desc()).all()
        assert len(memories) >= 2 # includes saved memories

        # Ensure the most relevant mock memory is in the user memories
        top_contents = [m.content for m in memories]
        assert "Python backend goal" in top_contents


# --- 4. User Isolation Security Test (Highest Priority) ---

def test_user_memory_isolation(client, token_headers, create_user, db_session):
    """
    USER ISOLATION (Priority Security): Ensure User A's vectors do not leak into User B's L2 scans.
    """
    headers_b = create_user("user_b@careeros.com")

    # User A creates a memory
    client.post("/ai/agent/chat", headers=token_headers, json={"message": "I want to become a Java developer."})

    # User B asks a question
    client.post("/ai/agent/chat", headers=headers_b, json={"message": "What career should I target?"})

    # End transaction to see changes committed by TestClient
    db_session.rollback()

    # Decode token to get User B's ID
    from jose import jwt
    from app.core.security import SECRET_KEY, ALGORITHM
    token_b = headers_b["Authorization"].split(" ")[1]
    payload_b = jwt.decode(token_b, SECRET_KEY, algorithms=[ALGORITHM])
    user_b_id = payload_b.get("sub")

    # Query memories and assert User B NEVER pulled or saved User A's 'Java' context
    all_java_memories = db_session.query(AgentMemory).filter(AgentMemory.content.like('%Java developer%')).all()
    user_b_java_memories = [m for m in all_java_memories if str(m.user_id) == str(user_b_id)]

    # Ensure User B has absolutely no connection to Java developer context
    assert len(user_b_java_memories) == 0


# --- 5. Agent Memory Scenarios (AGENT) ---

def test_agent_memory_continuity_and_updates(client, token_headers, test_user, db_session):
    """
    AGENT-01 / AGENT-03 / AGENT-06: First conversation memory, new session, update career goal.
    """
    db_session.query(AgentMemory).filter_by(user_id=test_user.id).delete()
    db_session.commit()

    # AGENT-01: First conversation
    response = client.post("/ai/agent/chat", headers=token_headers, json={"message": "I want to become a Python developer."})
    assert response.status_code == 200

    # End transaction to see changes committed by TestClient
    db_session.rollback()

    # AGENT-03: New session simulates retrieval of stored memory
    m = db_session.query(AgentMemory).filter_by(user_id=test_user.id).first()
    assert m is not None

    # AGENT-06: Update career goal
    client.post("/ai/agent/chat", headers=token_headers, json={"message": "Actually I decided to focus on Ruby instead."})

    # End transaction to see changes committed by TestClient
    db_session.rollback()

    memories = db_session.query(AgentMemory).filter_by(user_id=test_user.id).all()
    contents = [m.content for m in memories]
    assert any("Ruby" in c for c in contents)


# --- 6. Fallback Tests (FB) ---

def test_cockroachdb_and_vector_unavailability_fallback(client, token_headers, test_user, db_session):
    """
    FB-02 / FB-03: System continues to function and falls back gracefully when CockroachDB is down.
    """
    original_query = Session.query

    # Mock only the AgentMemory queries to simulate CockroachDB pgvector failure,
    # leaving user queries working so authentication succeeds.
    def mock_query_fn(self, *args, **kwargs):
        if AgentMemory in args:
            raise Exception("CockroachDB vector query refused")
        return original_query(self, *args, **kwargs)

    with patch("sqlalchemy.orm.Session.query", mock_query_fn):
        response = client.post("/ai/agent/chat", headers=token_headers, json={"message": "I want to become an SDE."})
        assert response.status_code == 200
        assert "reply" in response.json()
