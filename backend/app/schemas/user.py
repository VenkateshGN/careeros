from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    profile_image: Optional[str] = None
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
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )