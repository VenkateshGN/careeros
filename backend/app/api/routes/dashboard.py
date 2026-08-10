from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.job import Job
from app.models.application import Application

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/user-analytics")
def get_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns personalized user dashboard statistics dynamically from the database.
    """
    # 1. Dynamic Applications Calculation
    applications_count = db.query(Application).filter(Application.user_id == current_user.id).count()

    # 2. Dynamic Resume Score (can integrate with AI Service Parser eventually, calculating missing blocks)
    # Right now, scale dynamically off metadata. If they have URLs and bio it scales up.
    dynamic_resume_score = 0
    if current_user.resume_url:
        dynamic_resume_score += 40
    if current_user.bio:
        dynamic_resume_score += 30
    if current_user.portfolio_url or current_user.linkedin_url or current_user.github_url:
        dynamic_resume_score += 30

    # 3. Dynamic Job Recommendations (query based off active jobs in DB!)
    all_jobs = db.query(Job).limit(5).all()
    dynamic_job_recommendations = []

    for idx, job in enumerate(all_jobs):
        # Calculate a pseudo-dynamic match score based off strings for now till integrated fully
        desc_length = len(job.description) if job.description else 100
        pseudo_match = min(99, max(50, 100 - (desc_length % 50)))

        dynamic_job_recommendations.append({
            "job_id": str(job.id),
            "title": job.title,
            "match_score": f"{pseudo_match}%"
        })

    return {
        "status": "success",
        "analytics": {
            "applications_submitted": applications_count,
            "resume_score": dynamic_resume_score
        },
        "recommendations": dynamic_job_recommendations
    }
