from sqlalchemy.orm import Session

from models.task import Task


def create_task(db: Session, task: Task) -> Task:
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_task_by_id(
    db: Session,
    task_id: int
) -> Task | None:

    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )


def get_tasks_by_user(
    db: Session,
    user_id: int,
    completed: bool | None = None
) -> list[Task]:

    query = (
        db.query(Task)
        .filter(Task.user_id == user_id)
    )

    if completed is not None:
        query = query.filter(
            Task.completed == completed
        )

    return query.all()


def update_task_name(
    db: Session,
    task: Task,
    task_name: str
) -> Task:

    task.task_name = task_name

    db.commit()
    db.refresh(task)

    return task


def update_task_description(
    db: Session,
    task: Task,
    description: str | None
) -> Task:

    task.description = description

    db.commit()
    db.refresh(task)

    return task


def update_task_status(
    db: Session,
    task: Task,
    completed: bool
) -> Task:

    task.completed = completed

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task
) -> None:

    db.delete(task)
    db.commit()