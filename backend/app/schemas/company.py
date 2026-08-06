from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None

class CompanyResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
