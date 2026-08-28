import logging

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database import get_db

from schemas.admin import AdminUserTaskStats

from services.admin import get_users_with_task_stats

from security.dependencies import get_current_admin


# Logger for this module
logger = logging.getLogger(__name__)


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
    current_admin=Depends(get_current_admin)
):
    users = get_users_with_task_stats(db)

    logger.info(
        "Admin accessed user task statistics: admin_id=%s",
        current_admin.id
    )

    return users