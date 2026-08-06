from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.job import Job
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationResponse

router = APIRouter(
    tags=["Applications"]
)

@router.post("/jobs/{job_id}/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_for_job(
    job_id: UUID, 
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if already applied
    existing_application = db.query(Application).filter(
        Application.job_id == job_id,
        Application.user_id == current_user.id
    ).first()
    if existing_application:
        raise HTTPException(status_code=400, detail="Already applied to this job")

    if not current_user.resume_url:
        raise HTTPException(status_code=400, detail="Please upload a resume first before applying for jobs")

    application = Application(
        user_id=current_user.id,
        job_id=job_id,
        resume_url=current_user.resume_url,
        status="Applied"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    db.refresh(application)

    return application

from typing import List

@router.get("/users/me/applications", response_model=List[ApplicationResponse])
def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    apps = db.query(Application).filter(Application.user_id == current_user.id).all()
    return apps

@router.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def withdraw_application(
    application_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    db.delete(application)
    db.commit()
    return None
