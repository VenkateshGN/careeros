from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import TokenResponse

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