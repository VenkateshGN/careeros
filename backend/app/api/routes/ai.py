from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.ai import (
    ResumeReviewRequest, ResumeReviewResponse,
    CareerRoadmapRequest, CareerRoadmapResponse,
    MockInterviewRequest, MockInterviewResponse,
    ResumeSuggestionRequest, ResumeSuggestionResponse
)
from app.services import ai_service

router = APIRouter(
    prefix="/ai",
    tags=["AI Features"]
)

@router.post("/resume-review", response_model=ResumeReviewResponse)
def get_resume_review(
    request: ResumeReviewRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate an AI-powered resume review for a given resume_url.
    """
    review = ai_service.generate_resume_review(request.resume_url)
    return review

@router.post("/career-roadmap", response_model=CareerRoadmapResponse)
def get_career_roadmap(
    request: CareerRoadmapRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a stepped career roadmap.
    """
    roadmap = ai_service.generate_career_roadmap(request.current_role, request.target_role)
    return roadmap

@router.post("/mock-interview-questions", response_model=MockInterviewResponse)
def get_mock_interview_questions(request: MockInterviewRequest, current_user: User = Depends(get_current_user)):
    result = ai_service.generate_interview_questions_mock(request.job_title, request.industry)
    return result

@router.post("/resume-suggestions", response_model=ResumeSuggestionResponse)
def get_resume_suggestions(request: ResumeSuggestionRequest, current_user: User = Depends(get_current_user)):
    suggestions = ai_service.generate_resume_suggestions(request.job_title, request.experience_level)
    return {"suggestions": suggestions}
