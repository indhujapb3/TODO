import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.task import Task
from models.user import User

from schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse
)

from services.task import (
    create_user_task,
    get_user_tasks,
    get_user_task,
    update_user_task,
    update_user_task_status,
    delete_user_task
)

from security.dependencies import get_current_user


# Logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# CREATE TASK
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = create_user_task(
        db,
        task_data,
        current_user.id
    )

    logger.info(
        "Task created: task_id=%s user_id=%s",
        task.id,
        current_user.id
    )

    return task


# GET TASKS OF CURRENT USER
@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_tasks(
    completed: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = get_user_tasks(
        db,
        current_user.id,
        completed
    )

    logger.info(
        "Tasks retrieved: user_id=%s completed_filter=%s count=%s",
        current_user.id,
        completed,
        len(tasks)
    )

    return tasks


# GET ONE TASK
@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        task = get_user_task(
            db,
            task_id,
            current_user.id
        )

        logger.info(
            "Task retrieved: task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        return task

    except ValueError as e:

        logger.warning(
            "Task not found: task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except PermissionError as e:

        logger.warning(
            "Unauthorized task access: task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


# EDIT TASK
@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        task = update_user_task(
            db,
            task_id,
            current_user.id,
            task_data
        )

        logger.info(
            "Task updated: task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        return task

    except ValueError as e:

        logger.warning(
            "Task update failed - task not found: "
            "task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except PermissionError as e:

        logger.warning(
            "Unauthorized task update: task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


# UPDATE COMPLETED STATUS
@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse
)
def update_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        task = update_user_task_status(
            db,
            task_id,
            current_user.id,
            status_data
        )

        logger.info(
            "Task status updated: "
            "task_id=%s user_id=%s completed=%s",
            task_id,
            current_user.id,
            status_data.completed
        )

        return task

    except ValueError as e:

        logger.warning(
            "Task status update failed - task not found: "
            "task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except PermissionError as e:

        logger.warning(
            "Unauthorized task status update: "
            "task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


# DELETE TASK
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        delete_user_task(
            db,
            task_id,
            current_user.id
        )

        logger.info(
            "Task deleted: task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

    except ValueError as e:

        logger.warning(
            "Task deletion failed - task not found: "
            "task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except PermissionError as e:

        logger.warning(
            "Unauthorized task deletion: "
            "task_id=%s user_id=%s",
            task_id,
            current_user.id
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )