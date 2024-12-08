from fastapi import APIRouter

from backend.app.config import config

from .routes.auth import router as auth_router
from .routes.places import router as places_router
from .routes.users import router as users_router

router = APIRouter(
    prefix=config.api_prefix.v1.prefix,
)

router.include_router(auth_router)
router.include_router(places_router)
router.include_router(users_router)
