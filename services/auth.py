from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate

from app.repositories.user import (
    create_user,
    get_user_by_username,
)

from app.security.password import (
    hash_password,
    verify_password,
)

from app.security.jwt import create_access_token


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

    # Hash the password
    hashed_password = hash_password(
        user_data.password
    )

    # Create SQLAlchemy User model
    user = User(
        username=user_data.username,
        password=hashed_password,
        role="user"
    )

    # Save user
    return create_user(db, user)


def login_user(
    db: Session,
    login_data: LoginRequest
) -> TokenResponse:

    # Find user by username
    user = get_user_by_username(
        db,
        login_data.username
    )

    # User doesn't exist
    if user is None:
        raise ValueError("Invalid username or password")

    # Verify password
    password_valid = verify_password(
        login_data.password,
        user.password
    )

    # Password is incorrect
    if not password_valid:
        raise ValueError("Invalid username or password")

    # Create JWT
    access_token = create_access_token(
        user_id=user.id,
        role=user.role
    )

    # Return token response
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )