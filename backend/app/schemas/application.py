from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict
from app.schemas.job import JobResponse


class ApplicationCreate(BaseModel):
    pass
    # We don't really need anything in request body except maybe a note or something, 
    # but the path params have the job_id. Resume is taken from user.resume_url.


class ApplicationResponse(BaseModel):
    id: UUID
    user_id: UUID
    job_id: UUID
    resume_url: Optional[str] = None
    status: str
    applied_at: datetime
    updated_at: datetime

    job: Optional[JobResponse] = None

    model_config = ConfigDict(from_attributes=True)
