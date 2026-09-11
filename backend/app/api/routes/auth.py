from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.orm import Session
import secrets
import hashlib
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, hash_password
from app.models.user import User
from app.models.password_reset import PasswordReset
from app.schemas.auth import TokenResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.services.email_service import send_password_reset_email

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    username: str = Form(None),
    password: str = Form(None),
    request: Request = None,
    db: Session = Depends(get_db)
):
    email = username
    pass_val = password

    # If form fields are empty, fall back to parsing JSON body (for standard API/test requests)
    if not email or not pass_val:
        try:
            body = await request.json()
            email = body.get("email") or body.get("username")
            pass_val = body.get("password")
        except Exception:
            pass

    if not email or not pass_val:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing username/email or password"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or not verify_password(pass_val, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            return {"message": "If the email is registered, a password reset link has been sent."}

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        expires_at = datetime.utcnow() + timedelta(hours=1)
        reset_entry = PasswordReset(
            id=uuid.uuid4(),
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            used=False
        )
        db.add(reset_entry)
        db.commit()

        send_password_reset_email(user.email, token)

        return {"message": "If the email is registered, a password reset link has been sent."}
    except Exception as e:
        import logging
        logging.getLogger("careeros.auth").error(f"Forgot password error: {e}", exc_info=True)
        return {"message": "If the email is registered, a password reset link has been sent."}

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or token"
        )

    # Compute SHA-256 hash of incoming token
    incoming_hash = hashlib.sha256(data.token.encode()).hexdigest()

    # Query matching token
    reset_entry = db.query(PasswordReset).filter(
        PasswordReset.user_id == user.id,
        PasswordReset.token_hash == incoming_hash,
        PasswordReset.used == False,
        PasswordReset.expires_at > datetime.utcnow()
    ).first()

    if not reset_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token, expired, or already used"
        )

    # Update user password using bcrypt hash
    user.password_hash = hash_password(data.new_password)

    # Invalidate reset token
    reset_entry.used = True

    db.commit()
    return {"message": "Password has been successfully reset."}