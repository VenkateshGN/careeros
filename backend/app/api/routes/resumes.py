from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os
import uuid

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.services.resume_parser import extract_text_from_pdf

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_resume(
    resume: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate unique filename
    file_extension = resume.filename.split(".")[-1] if resume.filename else "pdf"
    unique_filename = f"{current_user.id}_{uuid.uuid4().hex[:8]}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    file_bytes = resume.file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(file_bytes)
        
    resume_url = f"/{file_path}"
    
    # Update user DB record
    current_user.resume_url = resume_url
    db.commit()
    db.refresh(current_user)
    
    # Parse PDF Text
    parsed_text = extract_text_from_pdf(file_bytes)
    
    # Process through an AI logic model to get structured data
    from app.services.ai_service import extract_structured_resume_data
    structured_data = extract_structured_resume_data(parsed_text)
    
    return {
        "resume_url": current_user.resume_url, 
        "message": "Resume uploaded successfully",
        "parsed_content_length": len(parsed_text),
        "structured_data": structured_data
    }

@router.delete("/")
def delete_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.resume_url:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No resume uploaded")
        
    file_path = current_user.resume_url.lstrip("/")
    if os.path.exists(file_path):
        os.remove(file_path)
        
    current_user.resume_url = None
    db.commit()
    db.refresh(current_user)
    return {"message": "Resume deleted successfully"}

@router.get("/download")
def download_resume(
    current_user: User = Depends(get_current_user)
):
    if not current_user.resume_url:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No resume uploaded")
        
    from fastapi.responses import FileResponse
    file_path = current_user.resume_url.lstrip("/")
    if not os.path.exists(file_path):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Resume file not found")
        
    return FileResponse(path=file_path, filename="resume.pdf", media_type="application/pdf")
