from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate

from app.repositories.user import (
    create_user,
    get_user_by_username,
)


def register_user(
    db: Session,
    user_data: UserCreate
) -> User:

    # Check whether username already exists
    existing_user = get_user_by_username(
        db,
        user_data.username
    )

    if existing_user:
        raise ValueError("Username already exists")

    # Create user
    user = User(
        username=user_data.username,
        password=user_data.password,
        role="user"
    )

    return create_user(db, user)


def authenticate_user(
    db: Session,
    login_data: LoginRequest
) -> User | None:

    # Find user by username
    user = get_user_by_username(
        db,
        login_data.username
    )

    if user is None:
        return None

    # Temporary password check
    if user.password != login_data.password:
        return None

    return user