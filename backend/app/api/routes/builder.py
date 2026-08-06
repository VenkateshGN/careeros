import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.builder import BuiltResume
from app.schemas.builder import BuiltResumeCreate, BuiltResumeUpdate, BuiltResumeResponse

router = APIRouter(
    prefix="/builder",
    tags=["Resume Builder"]
)

@router.post("/resume", response_model=BuiltResumeResponse, status_code=status.HTTP_201_CREATED)
def create_draft(
    draft_data: BuiltResumeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    draft = BuiltResume(
        user_id=current_user.id,
        template_id=draft_data.template_id,
        content=json.dumps(draft_data.content)
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft

@router.put("/resume/{draft_id}", response_model=BuiltResumeResponse)
def update_draft(
    draft_id: UUID,
    draft_data: BuiltResumeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    draft = db.query(BuiltResume).filter(BuiltResume.id == draft_id, BuiltResume.user_id == current_user.id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
        
    if draft_data.template_id:
        draft.template_id = draft_data.template_id
    if draft_data.content:
        draft.content = json.dumps(draft_data.content)
        
    db.commit()
    db.refresh(draft)
    return draft

@router.get("/resume/{draft_id}/export")
def export_draft_as_mock_pdf(
    draft_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    In a real setting, you would pass draft.content to ReportLab or a Node.js Puppeteer layer to generate a PDF.
    Here we return a mock file to simulate the endpoint output payload.
    """
    draft = db.query(BuiltResume).filter(BuiltResume.id == draft_id, BuiltResume.user_id == current_user.id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
        
    # Return raw text structure as simulated PDF wrapper output
    return JSONResponse(
        content={
            "pdf_status": "generated", 
            "url": f"/downloads/mock_resume_{draft_id}.pdf",
            "extracted_sections": json.loads(draft.content)
        }
    )
