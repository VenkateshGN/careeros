from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db, get_current_user
from app.schemas.interview import InterviewSimulation, InterviewSimulationCreate, InterviewQuestion
from app.models.user import User
import uuid
from datetime import datetime
from app.models.interview import InterviewSimulationModelMock

router = APIRouter()

mock_interviews = []
mock_questions = [
    InterviewQuestion(id="q1", question="Tell me about yourself.", expected_answer_keywords=["experience", "background", "passionate"], type="hr"),
    InterviewQuestion(id="q2", question="Explain REST APIs.", expected_answer_keywords=["http", "methods", "stateless", "endpoints"], type="technical")
]

@router.post("/start", response_model=InterviewSimulation)
def start_interview(data: InterviewSimulationCreate, current_user: User = Depends(get_current_user)):
    new_sim = InterviewSimulationModelMock(
        id=str(uuid.uuid4()),
        user_id=str(current_user.id),
        job_id=data.job_id,
        job_title=data.job_title,
        status="in_progress",
        score=None,
        feedback=None,
        created_at=datetime.utcnow()
    )
    mock_interviews.append(new_sim)
    return new_sim

@router.get("/{interview_id}/questions", response_model=List[InterviewQuestion])
def get_questions(interview_id: str, current_user: User = Depends(get_current_user)):
    return mock_questions

@router.post("/{interview_id}/submit")
def submit_interview(interview_id: str, current_user: User = Depends(get_current_user)):
    for sim in mock_interviews:
        if sim.id == interview_id and sim.user_id == str(current_user.id):
            sim.status = "completed"
            sim.score = 85
            sim.feedback = "Good technical answers, could improve soft skills phrasing."
            return sim
    raise HTTPException(status_code=404, detail="Interview not found")
