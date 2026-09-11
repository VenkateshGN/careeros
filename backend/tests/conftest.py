import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.agent_memory import AgentMemory

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture
def test_user(db_session):
    email = f"testuser_{uuid.uuid4()}@gmail.com"
    password = "password123"
    from app.core.security import hash_password
    user = User(
        id=uuid.uuid4(),
        full_name="Test User",
        email=email,
        password_hash=hash_password(password),
        role="candidate"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    yield user
    try:
        db_session.query(AgentMemory).filter_by(user_id=user.id).delete()
        db_session.delete(user)
        db_session.commit()
    except Exception:
        db_session.rollback()

@pytest.fixture
def token_headers(client, test_user):
    password = "password123"
    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user.email,
            "password": password
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def create_user(client, db_session):
    created_users = []

    def _create_user(email: str, password: str = "password123", role: str = "candidate"):
        unique_email = f"{uuid.uuid4()}_{email}"
        from app.core.security import hash_password
        user = User(
            id=uuid.uuid4(),
            full_name="Created User",
            email=unique_email,
            password_hash=hash_password(password),
            role=role
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        created_users.append(user)

        login_response = client.post(
            "/auth/login",
            json={
                "email": unique_email,
                "password": password
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    yield _create_user

    try:
        for user in created_users:
            db_session.query(AgentMemory).filter_by(user_id=user.id).delete()
            existing = db_session.query(User).filter(User.id == user.id).first()
            if existing:
                db_session.delete(existing)
        db_session.commit()
    except Exception:
        db_session.rollback()
