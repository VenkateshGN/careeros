from pydantic import BaseModel, BaseModel as SchemaBaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserAnalytics(SchemaBaseModel):
    user_id: str
    total_applications: int
    interviews_scheduled: int
    offers_received: int
    rejection_rate: float
    skill_growth: Dict[str, int] # e.g., {"python": +5, "react": +2}
    updated_at: datetime

class JobAnalytics(SchemaBaseModel):
    job_id: str
    total_views: int
    total_applications: int
    average_match_score: float
    updated_at: datetime
