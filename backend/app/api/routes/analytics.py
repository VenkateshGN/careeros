from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.schemas.analytics import UserAnalytics, JobAnalytics
from app.models.user import User
from datetime import datetime
from app.models.analytics import UserAnalyticsModelMock

router = APIRouter()

@router.get("/user", response_model=UserAnalytics)
def get_user_analytics(current_user: User = Depends(get_current_user)):
    return UserAnalyticsModelMock(
        user_id=str(current_user.id),
        total_applications=15,
        interviews_scheduled=3,
        offers_received=1,
        rejection_rate=0.2,
        skill_growth={"Python": 10, "FastAPI": 15},
        updated_at=datetime.utcnow()
    )

@router.get("/jobs/{job_id}", response_model=JobAnalytics)
def get_job_analytics(job_id: str, current_user: User = Depends(get_current_user)):
    # Assuming role checks inside services for real apps
    return JobAnalytics(
        job_id=job_id,
        total_views=1500,
        total_applications=300,
        average_match_score=75.5,
        updated_at=datetime.utcnow()
    )
