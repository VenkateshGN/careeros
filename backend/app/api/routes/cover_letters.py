from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db, get_current_user
from app.schemas.cover_letter import CoverLetter, CoverLetterCreate
from app.models.user import User
import uuid
from datetime import datetime
from app.models.cover_letter import CoverLetterModelMock

router = APIRouter()

# In-memory storage for mock
mock_db = []

@router.post("/generate", response_model=CoverLetter)
def generate_cover_letter(data: CoverLetterCreate, current_user: User = Depends(get_current_user)):
    # Mock AI Service Generation
    generated_content = f"Dear Hiring Manager at {data.company_name},\n\nI am thrilled to apply for the {data.job_title} role..."

    new_cl = CoverLetterModelMock(
        id=str(uuid.uuid4()),
        user_id=str(current_user.id),
        job_id=data.job_id,
        company_name=data.company_name,
        job_title=data.job_title,
        content=generated_content,
        tone=data.tone,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_db.append(new_cl)
    return new_cl

@router.get("/", response_model=List[CoverLetter])
def get_cover_letters(current_user: User = Depends(get_current_user)):
    user_cls = [cl for cl in mock_db if cl.user_id == str(current_user.id)]
    return user_cls

@router.delete("/{cl_id}")
def delete_cover_letter(cl_id: str, current_user: User = Depends(get_current_user)):
    global mock_db
    mock_db = [cl for cl in mock_db if not (cl.id == cl_id and cl.user_id == str(current_user.id))]
    return {"message": "Deleted successfully"}
