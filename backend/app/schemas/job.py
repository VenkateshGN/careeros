from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    description: str
    company_id: UUID
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company_id: Optional[UUID] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None


class JobResponse(BaseModel):
    id: UUID
    title: str
    description: str
    company_id: Optional[UUID] = None
    recruiter_id: Optional[UUID] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    posted_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
