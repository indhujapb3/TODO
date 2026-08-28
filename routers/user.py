import logging

from fastapi import APIRouter, Depends

from models.user import User

from schemas.user import UserResponse

from security.dependencies import get_current_user


# Logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    logger.info(
        "User profile accessed: user_id=%s username=%s",
        current_user.id,
        current_user.username
    )

    return current_user