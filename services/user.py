from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate
from repositories.user import (
    create_user,
    get_user_by_id,
    get_user_by_username,
)


def register_user(
    db: Session,
    user_data: UserCreate
) -> User:

    # Check if username already exists
    existing_user = get_user_by_username(
        db,
        user_data.username
    )

    if existing_user:
        raise ValueError("Username already exists")

    # Create SQLAlchemy User model
    user = User(
        username=user_data.username,
        password=user_data.password,
        role="user"
    )

    # Save user using repository
    return create_user(db, user)


def get_user(
    db: Session,
    user_id: int
) -> User | None:

    return get_user_by_id(db, user_id)