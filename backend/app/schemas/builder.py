from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
import json

class BuiltResumeCreate(BaseModel):
    template_id: Optional[str] = "default"
    content: Dict[str, Any]

class BuiltResumeUpdate(BaseModel):
    template_id: Optional[str] = None
    content: Optional[Dict[str, Any]] = None

class BuiltResumeResponse(BaseModel):
    id: UUID
    user_id: UUID
    template_id: str
    content: str  # Kept as string since it's Text on DB
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
