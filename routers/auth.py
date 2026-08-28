import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db

from schemas.user import (
    UserCreate,
    UserResponse
)

from schemas.auth import (
    LoginRequest,
    TokenResponse
)

from services.auth import (
    register_user,
    login_user
)


# Create logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        user = register_user(
            db,
            user_data
        )

        # Log successful registration
        logger.info(
            "User registered successfully: username=%s",
            user_data.username
        )

        return user

    except ValueError as e:

        # Log failed registration
        logger.warning(
            "User registration failed: username=%s reason=%s",
            user_data.username,
            str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        token_response = login_user(
            db,
            login_data
        )

        # Log successful login
        logger.info(
            "User logged in successfully: username=%s",
            login_data.username
        )

        return token_response

    except ValueError as e:

        # Log failed login
        logger.warning(
            "User login failed: username=%s reason=%s",
            login_data.username,
            str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )