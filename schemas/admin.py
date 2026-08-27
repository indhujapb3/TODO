from pydantic import BaseModel


class AdminUserTaskStats(BaseModel):
    user_id: int
    username: str
    total_tasks: int
    pending_tasks: int
    completed_tasks: int