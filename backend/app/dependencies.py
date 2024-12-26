import redis

from backend.app.config import config
from backend.core.services.jwt_service import JwtService
from backend.core.services.sms_service import SMSService
from backend.core.services.telegram_service import TelegramService
from backend.core.services.websocket import WebsocketService
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.setup import create_engine, create_session_pool

engine = create_engine(config.db)
session_pool = create_session_pool(engine)


def get_websocket_service():
    return WebsocketService()


async def get_repo():
    async with session_pool() as session:
        yield RequestsRepo(session)


def get_sms_service() -> SMSService:
    return SMSService()


def get_jwt_service() -> JwtService:
    return JwtService(
        secret_key=config.access_token.token_secret,
        algorithm=config.access_token.algorith,
        expire_time=config.access_token.token_expire_seconds,
    )


def get_telegram_service():
    return TelegramService()


def get_redis():
    return redis.Redis(
        host=config.redis.redis_host,
        port=config.redis.redis_port,
        decode_responses=True,
    )
