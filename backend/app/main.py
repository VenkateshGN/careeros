import logging
from fastapi import FastAPI

from app.api.routes import users
from app.api.routes import auth
from app.api.routes import resumes
from app.api.routes import jobs
from app.api.routes import applications
from app.api.routes import ai
from app.api.routes import notifications
from app.api.routes import admin
from app.api.routes import dashboard
from app.api.routes import companies
from app.api.routes import candidates
from app.api.routes import builder


app = FastAPI(
    title="CareerOS API"
)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(ai.router)
app.include_router(notifications.router)
app.include_router(admin.router)
app.include_router(dashboard.router)
app.include_router(companies.router)
app.include_router(candidates.router)
app.include_router(builder.router)


# -- Logging Configuration --
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("careeros.main")

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