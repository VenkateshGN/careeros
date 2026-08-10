from typing import List
from uuid import UUID
import time
import urllib.request
import json
import logging
import uuid as py_uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.job import Job
from app.models.application import Application
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.schemas.application import ApplicationResponse

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

logger = logging.getLogger("careeros.jobs")

_COMBINED_CACHE = {
    "jobs": [],
    "last_fetched": 0
}

def fetch_combined_jobs() -> list:
    now = time.time()
    # Cache for 15 minutes (900 seconds)
    if _COMBINED_CACHE["jobs"] and (now - _COMBINED_CACHE["last_fetched"] < 900):
        logger.info("Returning cached combined jobs")
        return _COMBINED_CACHE["jobs"]

    logger.info("Fetching fresh remote jobs from Remotive & Arbeitsagentur...")
    combined = []

    # 1. Fetch from Remotive API
    try:
        req = urllib.request.Request(
            'https://remotive.com/api/remote-jobs?category=software-dev&limit=30',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        remotive_jobs = data.get("jobs", [])
        for rj in remotive_jobs:
            job_uuid = py_uuid.uuid5(py_uuid.NAMESPACE_DNS, f"remotive_{rj.get('id')}")
            combined.append({
                "id": job_uuid,
                "title": rj.get("title", "Software Engineer"),
                "description": rj.get("description", "No description provided."),
                "company_id": None,
                "company_name": rj.get("company_name", "CareerOS Partner"),
                "company_logo": rj.get("company_logo") or rj.get("company_logo_url"),
                "company_website": rj.get("url"),
                "recruiter_id": None,
                "location": rj.get("candidate_required_location") or "Remote",
                "salary_min": None,
                "salary_max": None,
                "posted_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "match_score": None,
                "referenznummer": None
            })
    except Exception as e:
        logger.error(f"Failed to fetch Remotive jobs: {e}")

    # 2. Fetch from Arbeitsagentur API
    try:
        req = urllib.request.Request(
            'https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs?was=Softwareentwickler&size=30',
            headers={
                'X-API-Key': 'jobboerse-jobsuche',
                'User-Agent': 'Mozilla/5.0'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        ba_jobs = data.get("ergebnisliste", [])
        for rj in ba_jobs:
            refnr = rj.get("referenznummer")
            if not refnr:
                continue
            job_uuid = py_uuid.uuid5(py_uuid.NAMESPACE_DNS, f"arbeitsagentur_{refnr}")

            # Extract location
            loc_val = "Germany"
            locs = rj.get("stellenlokationen", [])
            if locs:
                loc_val = locs[0].get("adresse", {}).get("ort") or "Germany"

            combined.append({
                "id": job_uuid,
                "title": rj.get("stellenangebotsTitel", "Softwareentwickler"),
                "description": f"Open software engineering position at {rj.get('firma')}. Click View More to load details.",
                "company_id": None,
                "company_name": rj.get("firma", "German tech employer"),
                "company_logo": None,
                "company_website": f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{refnr}",
                "recruiter_id": None,
                "location": loc_val,
                "salary_min": None,
                "salary_max": None,
                "posted_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "match_score": None,
                "referenznummer": refnr
            })
    except Exception as e:
        logger.error(f"Failed to fetch Arbeitsagentur jobs: {e}")

    if combined:
        _COMBINED_CACHE["jobs"] = combined
        _COMBINED_CACHE["last_fetched"] = now

    return _COMBINED_CACHE["jobs"] or combined

@router.get("/", response_model=List[JobResponse])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = fetch_combined_jobs()
    if not jobs:
        # Fallback to database jobs if API fetch fails and cache is empty
        return db.query(Job).offset(skip).limit(limit).all()
    return jobs[skip : skip + limit]

@router.get("/suggestions", response_model=List[JobResponse])
def get_job_suggestions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    import os
    from app.services.resume_parser import extract_text_from_pdf
    from app.services import ai_service

    jobs = fetch_combined_jobs()
    if not jobs:
        jobs = [
            {
                "id": j.id,
                "title": j.title,
                "description": j.description,
                "company_id": j.company_id,
                "company_name": j.company_name,
                "company_logo": j.company_logo,
                "company_website": j.company_website,
                "recruiter_id": j.recruiter_id,
                "location": j.location,
                "salary_min": j.salary_min,
                "salary_max": j.salary_max,
                "posted_at": j.posted_at,
                "updated_at": j.updated_at,
                "match_score": None
            } for j in db.query(Job).all()
        ]

    if not jobs:
        return []

    # If user has neither resume nor skills, return no suggestions
    if not current_user.resume_url and not current_user.skills:
        return []

    # Try matching by resume
    resume_text = None
    if current_user.resume_url:
        file_path = current_user.resume_url.lstrip("/")
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                resume_text = extract_text_from_pdf(file_bytes)
            except Exception as e:
                pass

    if resume_text:
        jobs_list = [{"id": str(j["id"]), "title": j["title"], "description": j["description"] or ""} for j in jobs]
        try:
            ai_res = ai_service.rank_jobs_for_resume(resume_text, jobs_list)
            match_scores = {m["id"]: m["score"] for m in ai_res.get("matches", []) if "id" in m and "score" in m}

            suggested_jobs = []
            for job in jobs:
                score = match_scores.get(str(job["id"]), 0)
                if score >= 50:  # Only suggest related jobs (score >= 50%)
                    job_copy = dict(job)
                    job_copy["match_score"] = score
                    suggested_jobs.append(job_copy)

            suggested_jobs.sort(key=lambda j: j["match_score"] or 0, reverse=True)
            return suggested_jobs[:10]
        except Exception as e:
            pass # Fall back to skills match if AI ranking fails

    # Fallback to skills-based matching
    if not current_user.skills:
        return []

    user_skills = [s.strip().lower() for s in current_user.skills.split(",") if s.strip()]
    if not user_skills:
        return []

    suggested_jobs = []
    for job in jobs:
        matches_count = 0
        desc = (job["description"] or "").lower()
        title = (job["title"] or "").lower()
        for skill in user_skills:
            if skill in desc or skill in title:
                matches_count += 1

        if len(user_skills) > 0:
            score = int((matches_count / len(user_skills)) * 100)
        else:
            score = 0

        score = min(100, max(0, score))
        if score > 0:  # Only suggest related jobs (matches at least one skill)
            job_copy = dict(job)
            job_copy["match_score"] = score
            suggested_jobs.append(job_copy)

    suggested_jobs.sort(key=lambda j: j["match_score"] or 0, reverse=True)
    return suggested_jobs[:10]

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    import base64
    # Check cache first
    jobs = fetch_combined_jobs()
    for j in jobs:
        if j["id"] == job_id:
            # If it is an Arbeitsagentur job and description is not loaded yet
            if j.get("referenznummer") and "Click View More" in j["description"]:
                try:
                    refnr = j["referenznummer"]
                    ref_b64 = base64.b64encode(refnr.encode()).decode()
                    req = urllib.request.Request(
                        f'https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobdetails/{ref_b64}',
                        headers={'X-API-Key': 'jobboerse-jobsuche', 'User-Agent': 'Mozilla/5.0'}
                    )
                    with urllib.request.urlopen(req, timeout=5) as response:
                        det = json.loads(response.read().decode())
                        description = det.get("stellenangebotsBeschreibung") or "No description provided."
                        j["description"] = description
                except Exception as e:
                    logger.error(f"Failed to load details for refnr {j.get('referenznummer')}: {e}")
            return j

    # Fallback to database lookup
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can post jobs")

    new_job = Job(**job_data.model_dump(), recruiter_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/{job_id}/applicants", response_model=List[ApplicationResponse])
def get_job_applicants(
    job_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "recruiter":
        raise HTTPException(status_code=403, detail="Only recruiters can view applicants")

    # Check if job belongs to recruiter
    job = db.query(Job).filter(Job.id == job_id, Job.recruiter_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or unauthorized")

    applications = db.query(Application).filter(Application.job_id == job_id).all()
    return applications

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: UUID, job_data: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    update_dict = job_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: UUID, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return None
