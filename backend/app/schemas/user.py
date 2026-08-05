from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )