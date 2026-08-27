from sqlalchemy.orm import Session

from repositories.admin import get_all_users_with_task_stats
from schemas.admin import AdminUserTaskStats


def get_users_with_task_stats(
    db: Session
) -> list[AdminUserTaskStats]:

    results = get_all_users_with_task_stats(db)

    return [
        AdminUserTaskStats(
            user_id=result.user_id,
            username=result.username,
            total_tasks=result.total_tasks or 0,
            pending_tasks=result.pending_tasks or 0,
            completed_tasks=result.completed_tasks or 0
        )
        for result in results
    ]