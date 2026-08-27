from sqlalchemy import func, case
from sqlalchemy.orm import Session

from models.user import User
from models.task import Task


def get_all_users_with_task_stats(
    db: Session
):
    results = (
        db.query(
            User.id.label("user_id"),
            User.username.label("username"),

            func.count(Task.id).label("total_tasks"),

            func.sum(
                case(
                    (Task.completed == False, 1),
                    else_=0
                )
            ).label("pending_tasks"),

            func.sum(
                case(
                    (Task.completed == True, 1),
                    else_=0
                )
            ).label("completed_tasks")
        )
        .outerjoin(
            Task,
            User.id == Task.user_id
        )
        .filter(
            User.role == "user"
        )
        .group_by(
            User.id,
            User.username
        )
        .all()
    )

    return results