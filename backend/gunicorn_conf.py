import os

port = os.getenv("PORT", "8000")
bind = f"0.0.0.0:{port}"
workers = int(os.getenv("GUNICORN_WORKERS", "1"))
worker_class = "uvicorn.workers.UvicornWorker"

loglevel = "info"
accesslog = "-"  # log access to stdout
errorlog = "-"   # log errors to stdout
