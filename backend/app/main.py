from fastapi import FastAPI

from app.api.routes import users


app = FastAPI(
    title="CareerOS API"
)


app.include_router(users.router)


@app.get("/")
def root():
    return {
        "message": "CareerOS API running"
    }