from fastapi import FastAPI

from database import Base, engine

from models.user import User
from models.task import Task

from routers import auth, user, task, admin


app = FastAPI(
    title="Todo Application",
    description="Todo application built with FastAPI, SQLAlchemy and SQLite",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Register routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {
        "message": "Todo API is running"
    }