from fastapi import APIRouter

from api.endpoints.memes import router as memes_router
from api.endpoints.user import router as user_router
from core.constants import MEMES_PREFIX, MEMES_TAG

main_router = APIRouter()
main_router.include_router(memes_router, prefix=MEMES_PREFIX, tags=[MEMES_TAG])
main_router.include_router(user_router)
