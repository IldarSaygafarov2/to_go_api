from fastapi import APIRouter

from backend.app.config import config
from .routes.auth import router as auth_router

router = APIRouter(
    prefix=config.api_prefix.v1.prefix,
)

router.include_router(auth_router)
