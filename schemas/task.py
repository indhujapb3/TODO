from pydantic import BaseModel


class TaskCreate(BaseModel):
    task_name: str
    category: str
    description: str | None = None


class TaskUpdate(BaseModel):
    task_name: str | None = None
    category: str | None = None
    description: str | None = None


class TaskStatusUpdate(BaseModel):
    completed: bool


class TaskResponse(BaseModel):
    id: int
    user_id: int
    task_name: str
    category: str
    description: str | None
    completed: bool

    model_config = {
        "from_attributes": True
    }