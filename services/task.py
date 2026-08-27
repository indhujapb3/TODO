from sqlalchemy.orm import Session

from models.task import Task
from schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
)

from repositories.task import (
    create_task,
    get_task_by_id,
    get_tasks_by_user,
    update_task_name,
    update_task_description,
    update_task_status,
    delete_task,
)


def create_user_task(
    db: Session,
    task_data: TaskCreate,
    user_id: int
) -> Task:

    task = Task(
        user_id=user_id,
        task_name=task_data.task_name,
        category=task_data.category,
        description=task_data.description,
        completed=False
    )

    return create_task(db, task)


def get_user_tasks(
    db: Session,
    user_id: int,
    completed: bool | None = None
) -> list[Task]:

    return get_tasks_by_user(
        db,
        user_id,
        completed
    )


def get_user_task(
    db: Session,
    task_id: int,
    user_id: int
) -> Task:

    task = get_task_by_id(db, task_id)

    if task is None:
        raise ValueError("Task not found")

    if task.user_id != user_id:
        raise PermissionError(
            "You do not have permission to access this task"
        )

    return task


def update_user_task(
    db: Session,
    task_id: int,
    user_id: int,
    task_data: TaskUpdate
) -> Task:

    task = get_user_task(
        db,
        task_id,
        user_id
    )

    if task_data.task_name is not None:
        task = update_task_name(
            db,
            task,
            task_data.task_name
        )

    if task_data.category is not None:
        task.category = task_data.category

    if task_data.description is not None:
        task = update_task_description(
            db,
            task,
            task_data.description
        )

    return task


def update_user_task_status(
    db: Session,
    task_id: int,
    user_id: int,
    status_data: TaskStatusUpdate
) -> Task:

    task = get_user_task(
        db,
        task_id,
        user_id
    )

    return update_task_status(
        db,
        task,
        status_data.completed
    )


def delete_user_task(
    db: Session,
    task_id: int,
    user_id: int
) -> None:

    task = get_user_task(
        db,
        task_id,
        user_id
    )

    delete_task(db, task)