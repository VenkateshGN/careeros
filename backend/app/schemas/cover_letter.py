from pydantic import BaseModel, BaseModel as SchemaBaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CoverLetterBase(SchemaBaseModel):
    job_id: Optional[str] = None
    company_name: str
    job_title: str
    content: str
    tone: Optional[str] = "professional"

class CoverLetterCreate(CoverLetterBase):
    pass

class CoverLetterUpdate(SchemaBaseModel):
    content: Optional[str] = None
    tone: Optional[str] = None

class CoverLetter(CoverLetterBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
