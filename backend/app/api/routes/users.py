from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_user

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserChangePassword
)

from app.services.user_service import create_user, update_user_profile, change_user_password


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)



@router.get(
    "/me",
    response_model=UserResponse
)
def get_current_user_data(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.put(
    "/me",
    response_model=UserResponse
)
def update_current_user_data(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_data = user_data.model_dump(exclude_unset=True, mode='json')
    return update_user_profile(db, current_user, update_data)


@router.put(
    "/change-password"
)
def change_password(
    password_data: UserChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    change_user_password(db, current_user, password_data.old_password, password_data.new_password)
    return {"message": "Password updated successfully"}


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user
