from fastapi import APIRouter

from api.endpoints.media_management import router as media_router
from api.endpoints.user import router as user_router
from core.constants import MEDIA_TAG

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(media_router, tags=[MEDIA_TAG])
