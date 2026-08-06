from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.job import Job
from app.models.application import Application

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/stats")
def get_admin_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Depending on production role management, check if current_user is admin.
    # For now, we just return stats to any authenticated user as a mockup.
    
    total_users = db.query(User).count()
    total_jobs = db.query(Job).count()
    total_applications = db.query(Application).count()
    
    return {
        "status": "success",
        "data": {
            "total_users": total_users,
            "total_jobs": total_jobs,
            "total_applications": total_applications
        }
    }
