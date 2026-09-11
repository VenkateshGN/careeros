
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

import re
import logging
from typing import Optional

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.agent_memory import AgentMemory

from app.schemas.ai import (
    ResumeReviewRequest,
    ResumeReviewResponse,
    CareerRoadmapRequest,
    CareerRoadmapResponse,
    MockInterviewRequest,
    MockInterviewResponse,
    ResumeSuggestionRequest,
    ResumeSuggestionResponse,
    JobMatchingRequest,
    JobMatchingResponse,
)

from app.services import ai_service


router = APIRouter(
    prefix="/ai",
    tags=["AI Features"]
)


# ============================================================
# Agent Chat Schemas
# ============================================================

class AgentChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class AgentChatResponse(BaseModel):
    reply: str


# ============================================================
# Memory Security / Sanitization
# ============================================================

def sanitize_memory_content(text: str) -> str:
    """
    Remove sensitive credentials and tokens before storing
    conversation data in the agent_memories table.
    """

    # 1. Redact JWT tokens
    text = re.sub(
        r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
        "[REDACTED_JWT]",
        text
    )

    # 2. Redact AWS Access Keys
    text = re.sub(
        r"AKIA[A-Z0-9]{16}",
        "[REDACTED_AWS_KEY]",
        text
    )

    # 3. Redact API keys / secrets / passwords / tokens
    text = re.sub(
        r"""(?i)
        (password|secret|api_key|private_key|token)
        ["']?\s*[:=]\s*["']?
        ([A-Za-z0-9_\-]{8,})
        ["']?
        """,
        r"\1: [REDACTED_SECRET]",
        text,
        flags=re.VERBOSE
    )

    return text


# ============================================================
# Agentic Memory Chat
# ============================================================

@router.post(
    "/agent/chat",
    response_model=AgentChatResponse
)
def agent_chat(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    CareerOS Agentic Memory endpoint.

    Flow:

    User message
        ↓
    Authenticated User Profile
        ↓
    Gemini Embedding
        ↓
    1536-dimensional vector
        ↓
    CockroachDB VECTOR(1536)
        ↓
    L2 similarity search
        ↓
    Top 4 memories
        ↓
    User Profile + Memories + Current Query
        ↓
    Gemini
        ↓
    AWS Bedrock fallback
        ↓
    AI response
        ↓
    Persist new memory
    """

    logger = logging.getLogger("careeros.ai_route")

    # ========================================================
    # 0. Authentication / User Profile
    # ========================================================

    logger.info("AI Chat Endpoint Entered")

    logger.info(
        f"Authenticated User ID: {current_user.id}"
    )

    logger.info(
        f"Session ID: {request.session_id}"
    )

    logger.info(
        f"Question: {request.message}"
    )

    # Log profile information for debugging
    logger.info(
        f"Authenticated User Name: "
        f"{current_user.full_name}"
    )

    logger.info(
        f"Authenticated User Skills: "
        f"{current_user.skills}"
    )

    logger.info(
        f"Authenticated User Role: "
        f"{current_user.role}"
    )

    # ========================================================
    # 1. Build User Profile Context
    # ========================================================

    profile_context = f"""
User Profile:

Name:
{current_user.full_name or "Not provided"}

Headline:
{current_user.headline or "Not provided"}

Bio:
{current_user.bio or "Not provided"}

Skills:
{current_user.skills or "Not provided"}

Role:
{current_user.role or "Not provided"}

Location:
{current_user.location or "Not provided"}

GitHub:
{current_user.github_url or "Not provided"}

LinkedIn:
{current_user.linkedin_url or "Not provided"}

Portfolio:
{current_user.portfolio_url or "Not provided"}

Resume:
{current_user.resume_url or "Not provided"}

Profile Verified:
{current_user.is_verified}
"""

    logger.info(
        "User profile context prepared"
    )

    # ========================================================
    # 2. Generate Gemini embedding for user query
    # ========================================================

    query_vector = None

    logger.info(
        "Calling generate_embeddings function..."
    )

    logger.info(
        "Embedding model: models/gemini-embedding-2"
    )

    try:

        query_vector = ai_service.generate_embeddings(
            request.message
        )

        if query_vector:

            logger.info(
                f"Embedding dimension generated: "
                f"{len(query_vector)}"
            )

    except Exception as e:

        logger.error(
            f"Failed to generate query embeddings: {e}",
            exc_info=True
        )

    # ========================================================
    # 3. Retrieve Semantic Memories
    # ========================================================

    memories = []

    vector_search_available = True

    if query_vector:

        logger.info(
            "VECTOR SEARCH STARTED"
        )

        logger.info(
            f"user_id={current_user.id}"
        )

        logger.info(
            f"query vector type={type(query_vector)}"
        )

        logger.info(
            f"query vector dimension={len(query_vector)}"
        )

        try:

            # Ensure embedding values are plain Python floats
            query_vector = [
                float(value)
                for value in query_vector
            ]

            # ------------------------------------------------
            # Validate Gemini embedding dimension
            # ------------------------------------------------

            if len(query_vector) != 1536:

                raise ValueError(
                    "Invalid embedding dimension. "
                    f"Expected 1536, "
                    f"received {len(query_vector)}."
                )

            # ------------------------------------------------
            # CockroachDB vector similarity search
            # ------------------------------------------------

            if db.bind.dialect.name in ('postgresql', 'cockroachdb'):
                memories = (
                    db.query(AgentMemory)
                    .filter(
                        AgentMemory.user_id == current_user.id
                    )
                    .order_by(
                        AgentMemory.embedding.l2_distance(
                            query_vector
                        )
                    )
                    .limit(4)
                    .all()
                )
            else:
                memories = (
                    db.query(AgentMemory)
                    .filter(
                        AgentMemory.user_id == current_user.id
                    )
                    .order_by(
                        AgentMemory.created_at.desc()
                    )
                    .limit(4)
                    .all()
                )

            logger.info(
                "VECTOR SEARCH SUCCESS | "
                f"user_id={current_user.id} | "
                f"query_embedding_dimension="
                f"{len(query_vector)} | "
                f"memories_found={len(memories)}"
            )

        except Exception as e:

            logger.error(
                "CockroachDB/pgvector vector "
                f"search failed: {e}",
                exc_info=True
            )

            vector_search_available = False

            db.rollback()

    # ========================================================
    # 4. Build Semantic Memory Context
    # ========================================================

    if memories:

        context_str = "\n".join(
            f"- {memory.content}"
            for memory in memories
        )

    else:

        context_str = (
            "No previous memory stored."
        )

    logger.info(
        f"Memory context prepared | "
        f"memories={len(memories)}"
    )

    # Log retrieved memories
    for i, memory in enumerate(
        memories,
        start=1
    ):

        logger.info(
            f"MEMORY {i}: {memory.content}"
        )

    # ========================================================
    # 5. Construct AI Prompt
    # ========================================================

    prompt = f"""
You are the CareerOS Agentic Memory System.

You are powered primarily by Google Gemini
with AWS Bedrock as a fallback provider.

============================================================
USER PROFILE
============================================================

{profile_context}

============================================================
RETRIEVED LONG-TERM MEMORIES
============================================================

The following information represents semantically relevant
long-term memories retrieved from CockroachDB:

{context_str}

============================================================
CURRENT USER QUERY
============================================================

{request.message}

============================================================
INSTRUCTIONS
============================================================

Use the user profile and retrieved memories when they are
relevant to the current question.

The user profile is authoritative for stable information
such as:

- Name
- Skills
- Role
- Location
- GitHub
- LinkedIn
- Portfolio
- Resume information

Use retrieved memories for:

- Previous conversations
- Previous questions
- Projects
- Preferences
- Decisions
- Long-term context

Do not invent information that is not present in:

1. The user profile
2. Retrieved memories
3. The current user query

If the requested information is unavailable in all three
sources, clearly say that you do not have that information.

Respond directly and naturally to the user.

Return ONLY a valid JSON object in this format:

{{
    "reply": "your conversational response"
}}
"""

    # ========================================================
    # 6. Determine AI Provider
    # ========================================================

    if ai_service.gemini_client:

        logger.info(
            "AI provider selected: Gemini"
        )

    elif ai_service.bedrock_client:

        logger.info(
            "AI provider selected: AWS Bedrock"
        )

    else:

        logger.info(
            "AI provider selected: "
            "None (static fallback)"
        )

    # ========================================================
    # 7. Generate AI Response
    # ========================================================

    user_name = getattr(current_user, "full_name", None) or "Candidate"
    msg_lower = request.message.lower()

    if any(k in msg_lower for k in ["knowledge", "about me", "who am i", "my profile"]):
        smart_reply = (
            f"Yes! I know you are {user_name} ({current_user.email}). "
            f"Your career profile, resume skills, and application history are indexed in your CareerOS workspace."
        )
    else:
        smart_reply = (
            f"I am currently experiencing technical difficulties connecting to AI providers. "
            f"Please try again later."
        )

    fallback_response = {
        "reply": smart_reply
    }

    logger.info(
        "Calling AI generation function..."
    )

    res = ai_service._call_bedrock_json(
        prompt,
        fallback_response
    )

    if isinstance(res, dict):

        reply = res.get(
            "reply",
            str(res)
        )

    else:

        reply = str(res)

    logger.info(
        f"AI response generated: "
        f"{reply[:100]}..."
    )

    # ========================================================
    # 8. Persist Conversation as Long-Term Memory
    # ========================================================

    if query_vector and vector_search_available:

        logger.info(
            "Persistence function database "
            "insert called..."
        )

        try:

            # Sanitize sensitive information
            sanitized_question = (
                sanitize_memory_content(
                    request.message
                )
            )

            sanitized_reply = (
                sanitize_memory_content(
                    reply
                )
            )

            # Create memory record
            new_mem = AgentMemory(

                user_id=current_user.id,

                content=(
                    f"User Question: "
                    f"{sanitized_question} "
                    f"| AI Answer Context: "
                    f"{sanitized_reply}"
                ),

                embedding=query_vector,

                session_id=request.session_id,

                metadata_={}
            )

            db.add(new_mem)

            db.commit()

            logger.info(
                "Memory persisted successfully"
            )

        except Exception as e:

            logger.error(
                "Failed to save agent memory "
                f"to CockroachDB: {e}",
                exc_info=True
            )

            db.rollback()

    # ========================================================
    # 9. Return Response to Frontend
    # ========================================================

    return {
        "reply": reply
    }


# ============================================================
# Resume Review
# ============================================================

@router.post(
    "/resume-review",
    response_model=ResumeReviewResponse
)
def get_resume_review(
    request: ResumeReviewRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate an AI-powered resume review.
    """

    review = ai_service.generate_resume_review(
        request.resume_url
    )

    return review


# ============================================================
# Job Matching
# ============================================================

@router.post(
    "/job-matching",
    response_model=JobMatchingResponse
)
def evaluate_job_match(
    request: JobMatchingRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Compare user's resume against a job description.
    """

    return ai_service.evaluate_job_match(
        request.resume_text,
        request.job_description
    )


# ============================================================
# Career Roadmap
# ============================================================

@router.post(
    "/career-roadmap",
    response_model=CareerRoadmapResponse
)
def get_career_roadmap(
    request: CareerRoadmapRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate a stepped career roadmap.
    """

    roadmap = ai_service.generate_career_roadmap(
        request.current_role,
        request.target_role
    )

    return roadmap


# ============================================================
# Mock Interview Questions
# ============================================================

@router.post(
    "/mock-interview-questions",
    response_model=MockInterviewResponse
)
def get_mock_interview_questions(
    request: MockInterviewRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate mock interview questions.
    """

    result = ai_service.generate_interview_questions(
        request.job_title,
        request.experience_level
    )

    return result


# ============================================================
# Resume Suggestions
# ============================================================

@router.post(
    "/resume-suggestions",
    response_model=ResumeSuggestionResponse
)
def get_resume_suggestions(
    request: ResumeSuggestionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate AI-powered resume suggestions.
    """

    suggestions = (
        ai_service.generate_resume_suggestions(
            request.job_title,
            request.experience_level
        )
    )

    return {
        "suggestions": suggestions
    }
