from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)

@router.get("/", response_model=List[UserResponse])
def search_candidates(
    skills: Optional[str] = None,
    location: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can search candidates")
        
    query = db.query(User).filter(User.role == "candidate")
    
    if skills:
        query = query.filter(User.skills.ilike(f"%{skills}%"))
    if location:
        query = query.filter(User.location.ilike(f"%{location}%"))
        
    return query.all()
