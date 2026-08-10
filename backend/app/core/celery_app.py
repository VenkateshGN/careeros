from celery import Celery

celery_app = Celery(
    "careeros_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def process_resume_parsing_task(resume_id: str):
    # Dummy worker task
    return f"Processed {resume_id}"

@celery_app.task
def generate_ai_cover_letter_background(job_id: str, user_id: str):
    # Background generation for long tasks
    return f"Cover letter generation done for {user_id}"
