import sys
from pathlib import Path

# Add backend directory to sys.path so 'app.*' imports resolve on Vercel Serverless
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
# from prometheus_fastapi_instrumentator import Instrumentator # Install in production

limiter = Limiter(key_func=get_remote_address)

from app.api.routes import users
from app.api.routes import auth
from app.api.routes import resumes
from app.api.routes import jobs
from app.api.routes import applications
from app.api.routes import ai
from app.api.routes import admin
from app.api.routes import dashboard
from app.api.routes import companies
from app.api.routes import candidates
from app.api.routes import builder
from app.api.routes import cover_letters
from app.api.routes import interviews
from app.api.routes import analytics

app = FastAPI(
    title="CareerOS API",
    description="The core backend API serving the AI-Driven CareerOS Platform. Features AI Interview Mocking, Resume Builders, and analytics tracking.",
    version="1.0.0",
    redirect_slashes=False,
    terms_of_service="http://careeros.com/terms/",
    contact={
        "name": "CareerOS Support",
        "url": "http://careeros.com/contact",
        "email": "support@careeros.com",
    },
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://your-production-app.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrumentator().instrument(app).expose(app) # Monitoring endpoint at /metrics

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(ai.router)
app.include_router(admin.router)
app.include_router(dashboard.router)
app.include_router(companies.router)
app.include_router(candidates.router, prefix="/api/v1/candidates", tags=["Candidates"])
app.include_router(builder.router, prefix="/api/v1/builder", tags=["Resume Builder"])
app.include_router(cover_letters.router, prefix="/api/v1/cover-letters", tags=["Cover Letters"])
app.include_router(interviews.router, prefix="/api/v1/interviews", tags=["Interviews"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

# -- Logging Configuration --
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("careeros.main")

@app.on_event("startup")
def sync_db():
    try:
        from app.core.database import engine, Base
        Base.metadata.create_all(bind=engine)
        from sqlalchemy import text
        with engine.begin() as conn:
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'candidate' NOT NULL;"))
            except Exception:
                pass
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN organization_id VARCHAR(100);"))
            except Exception:
                pass
    except Exception as e:
        logger.error(f"DB startup sync issue: {e}")

@app.get("/")
def root():
    logger.info("Root endpoint hit.")
    return {
        "message": "CareerOS API running"
    }

@app.get("/health", tags=["Monitoring"])
def health_check():
    """
    Monitoring endpoint used by Docker/AWS/GCP orchestration to verify API is healthy.
    """
    logger.info("Health check run.")
    return {"status": "ok", "service": "careeros-backend"}