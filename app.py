from fastapi import FastAPI

from app.routers import auth, user, task


app = FastAPI(
    title="Todo Application",
    description="Todo application built with FastAPI, SQLAlchemy and SQLite",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)


@app.get("/")
def root():
    return {
        "message": "Todo API is running"
    }