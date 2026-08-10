from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Optional[str] = "candidate"


from pydantic import HttpUrl

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    github_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None
    profile_image: Optional[HttpUrl] = None
    skills: Optional[str] = None


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    headline: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    profile_image: Optional[str] = None
    resume_url: Optional[str] = None
    skills: Optional[str] = None
    is_verified: bool = False
    role: str
    organization_id: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )