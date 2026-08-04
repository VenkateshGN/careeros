from fastapi import FastAPI

app = FastAPI(
    title="CareerOS API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "CareerOS Backend Running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }