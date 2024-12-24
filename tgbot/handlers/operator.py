from aiogram import Router
from aiogram.types import Message
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.filters.role import RoleFilter
from aiogram.filters import CommandStart

operator_router = Router()
operator_router.message.filter(RoleFilter())


@operator_router.message(CommandStart())
async def operator_start(message: Message, repo: "RequestsRepo"):
    operator = await repo.operators.get_operator_by_telegram_username(
        telegram_username=message.from_user.username
    )
    await message.answer(f"Hello operator, {operator.fullname}")
