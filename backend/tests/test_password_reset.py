import pytest
import uuid
import hashlib
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.password_reset import PasswordReset
from app.core.security import hash_password, verify_password

client = TestClient(app)

def test_password_reset_flow():
    db = SessionLocal()
    email = f"reset_test_{uuid.uuid4()}@gmail.com"
    raw_password = "old_password123"
    new_password = "new_password456"

    try:
        # 1. Create a user
        hashed = hash_password(raw_password)
        user = User(
            full_name="Reset Tester",
            email=email,
            password_hash=hashed,
            role="candidate"
        )
        db.add(user)
        db.commit()

        # 2. Trigger forgot-password
        forgot_res = client.post("/auth/forgot-password", json={"email": email})
        assert forgot_res.status_code == 200
        assert "password reset link" in forgot_res.json()["message"]

        # 3. Query token hash from database
        reset_entry = db.query(PasswordReset).filter(PasswordReset.user_id == user.id).first()
        assert reset_entry is not None
        assert reset_entry.used is False
        assert reset_entry.expires_at > datetime.utcnow()

        # Since we can't extract the raw token easily from the hash without knowing it,
        # let's mock/simulate the flow by creating a known token for verification.
        raw_token = "my-test-secure-reset-token-12345"
        test_hash = hashlib.sha256(raw_token.encode()).hexdigest()

        known_reset = PasswordReset(
            user_id=user.id,
            token_hash=test_hash,
            expires_at=datetime.utcnow() + timedelta(hours=1),
            used=False
        )
        db.add(known_reset)
        db.commit()

        # 4. Attempt reset password with invalid token
        bad_reset = client.post("/auth/reset-password", json={
            "email": email,
            "token": "wrong-token-abc",
            "new_password": new_password
        })
        assert bad_reset.status_code == 400

        # 5. Reset password with correct token
        good_reset = client.post("/auth/reset-password", json={
            "email": email,
            "token": raw_token,
            "new_password": new_password
        })
        assert good_reset.status_code == 200
        assert "successfully reset" in good_reset.json()["message"]

        # 6. Verify password updated in DB
        db.refresh(user)
        assert verify_password(new_password, user.password_hash)
        assert not verify_password(raw_password, user.password_hash)

        # 7. Verify token marked as used
        db.refresh(known_reset)
        assert known_reset.used is True

        # 8. Attempt reuse same token (fails)
        reuse_res = client.post("/auth/reset-password", json={
            "email": email,
            "token": raw_token,
            "new_password": "yet_another_password"
        })
        assert reuse_res.status_code == 400

        # 9. Test expired token
        expired_hash = hashlib.sha256("expired-token".encode()).hexdigest()
        expired_reset = PasswordReset(
            user_id=user.id,
            token_hash=expired_hash,
            expires_at=datetime.utcnow() - timedelta(minutes=1), # Already expired
            used=False
        )
        db.add(expired_reset)
        db.commit()

        exp_res = client.post("/auth/reset-password", json={
            "email": email,
            "token": "expired-token",
            "new_password": "new_password789"
        })
        assert exp_res.status_code == 400

    finally:
        # Clean up database records
        db.query(PasswordReset).filter(PasswordReset.user_id == user.id).delete()
        db.query(User).filter(User.id == user.id).delete()
        db.commit()
        db.close()
