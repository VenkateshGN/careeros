from pydantic import BaseModel, BaseModel as SchemaBaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class InterviewQuestion(SchemaBaseModel):
    id: str
    question: str
    expected_answer_keywords: List[str]
    type: str # technical, hr, behavioral

class InterviewSimulationBase(SchemaBaseModel):
    job_id: Optional[str] = None
    job_title: str
    status: str # setup, in_progress, completed
    score: Optional[int] = None
    feedback: Optional[str] = None

class InterviewSimulationCreate(InterviewSimulationBase):
    pass

class InterviewSimulationUpdate(SchemaBaseModel):
    status: Optional[str] = None
    score: Optional[int] = None
    feedback: Optional[str] = None

class InterviewSimulation(InterviewSimulationBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True
