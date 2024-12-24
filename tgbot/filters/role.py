from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

from config.loader import load_config
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.setup import create_engine, create_session_pool

config = load_config(".env")
engine = create_engine(config.db)
session_pool = create_session_pool(engine)


class RoleFilter(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        username = message.from_user.username

        async with session_pool() as session:
            repo = RequestsRepo(session)

            user = await repo.operators.get_operator_by_telegram_username(
                telegram_username=username
            )
            if not user:
                return False

            return True
