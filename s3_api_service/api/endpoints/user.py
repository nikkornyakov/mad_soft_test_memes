from fastapi import APIRouter

from core.constants import AUTH_PREFIX, AUTH_TAG
from core.user import auth_backend, fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=AUTH_PREFIX,
    tags=[AUTH_TAG],
)
