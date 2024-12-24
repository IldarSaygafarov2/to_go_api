from fastapi import APIRouter

from backend.app.config import config

from .routes.auth import router as auth_router
from .routes.chat import router as chat_router
from .routes.pages import router as pages_router
from .routes.places import router as places_router
from .routes.support import router as support_router
from .routes.users import router as users_router

router = APIRouter(
    prefix=config.api_prefix.v1.prefix,
)

router.include_router(auth_router)
router.include_router(places_router)
router.include_router(users_router)
router.include_router(pages_router)
router.include_router(chat_router)
router.include_router(support_router)
