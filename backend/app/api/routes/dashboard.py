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
    Returns personalized user dashboard statistics.
    """
    # Existent applications calculation
    applications_count = db.query(Application).filter(Application.user_id == current_user.id).count()
    
    # Mock resume score
    mock_resume_score = 92 if current_user.resume_url else 0
    
    # Mock targeted Job Recommendations generated using AI processing behind the scenes
    mock_job_recommendations = [
        {"job_id": "1", "title": "Senior AI Systems Engineer", "match_score": "95%"},
        {"job_id": "2", "title": "Lead Python Developer", "match_score": "88%"}
    ]
    
    return {
        "status": "success",
        "analytics": {
            "applications_submitted": applications_count,
            "resume_score": mock_resume_score
        },
        "recommendations": mock_job_recommendations
    }
