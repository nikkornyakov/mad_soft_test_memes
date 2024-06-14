from fastapi import APIRouter

from core.constants import (
    AUTH_PREFIX,
    AUTH_TAG,
    SIGNUP_PREFIX,
    SIGNUP_TAG,
    USER_PREFIX,
    USER_TAG,
)
from core.user import auth_backend, fastapi_users
from schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=AUTH_PREFIX,
    tags=[AUTH_TAG],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=SIGNUP_PREFIX,
    tags=[SIGNUP_TAG],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=USER_PREFIX,
    tags=[USER_TAG],
)
