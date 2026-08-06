# Use the official Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Upgrade pip and install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install PyPDF2 gunicorn  # Ensuring dynamic parser and production web servers are included

# Copy the actual application files
COPY ./app ./app
COPY ./alembic.ini .
COPY ./alembic ./alembic
COPY ./gunicorn_conf.py .

# Expose standard FastAPI port
EXPOSE 8000

# Run Uvicorn via Gunicorn when container launches
CMD ["gunicorn", "-c", "gunicorn_conf.py", "app.main:app"]
