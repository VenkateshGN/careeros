from typing import List, Optional
from pydantic import BaseModel

class ResumeReviewRequest(BaseModel):
    resume_url: str

class ResumeReviewResponse(BaseModel):
    overall_score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]

class CareerRoadmapRequest(BaseModel):
    current_role: str
    target_role: str

class RoadmapStep(BaseModel):
    step_number: int
    title: str
    description: str
    timeline: str

class CareerRoadmapResponse(BaseModel):
    target_role: str
    steps: List[RoadmapStep]

class InterviewQuestionsRequest(BaseModel):
    job_title: str
    experience_level: Optional[str] = "Mid level"

class MockInterviewQuestion(BaseModel):
    question: str
    category: str
    hint: str

class MockInterviewResponse(BaseModel):
    questions: List[MockInterviewQuestion]

class ResumeSuggestionRequest(BaseModel):
    job_title: str
    experience_level: str = "Mid-level"

class ResumeSuggestionResponse(BaseModel):
    suggestions: List[str]

class InterviewQuestion(BaseModel):
    question: str
    category: str
    hint: str

class InterviewQuestionsResponse(BaseModel):
    job_title: str
    questions: List[InterviewQuestion]
