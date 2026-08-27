from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.admin import AdminUserTaskStats
from services.admin import get_users_with_task_stats
from security.dependencies import get_current_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get(
    "/users",
    response_model=list[AdminUserTaskStats]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    return get_users_with_task_stats(db)