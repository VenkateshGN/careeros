from fastapi import HTTPException
from app.models.user import User
from app.core.security import hash_password



def create_user(db, user_data):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    hashed_password = hash_password(
        user_data.password
    )


    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hashed_password,
        role=getattr(user_data, "role", "candidate")
    )


    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user_profile(db, user: User, update_data: dict):
    for field, value in update_data.items():
        if value is not None:
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


def change_user_password(db, user: User, old_password: str, new_password: str):
    from app.core.security import verify_password
    
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )
        
    user.password_hash = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user