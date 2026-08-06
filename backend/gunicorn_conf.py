import os

bind = "0.0.0.0:8000"
workers = int(os.getenv("GUNICORN_WORKERS", "4"))
worker_class = "uvicorn.workers.UvicornWorker"

loglevel = "info"
accesslog = "-"  # log access to stdout
errorlog = "-"   # log errors to stdout
