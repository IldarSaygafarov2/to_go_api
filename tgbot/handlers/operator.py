import json
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from backend.app.dependencies import get_redis
from backend.core.interfaces.support import SupportMessage
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.filters.role import RoleFilter
from tgbot.misc.operator_state import OperatorState
from backend.core.services.websocket import WebsocketService

operator_router = Router()
operator_router.message.filter(RoleFilter())

websocket_service = WebsocketService()


@operator_router.message(CommandStart())
async def operator_start(message: Message, repo: "RequestsRepo", state: FSMContext):
    operator = await repo.operators.get_operator_by_telegram_username(
        telegram_username=message.from_user.username
    )
    await repo.operators.update_telegram_chat_id(
        operator_id=operator.id, telegram_chat_id=message.from_user.id
    )
    print("telegram chat id updated")
    await message.answer(f"Hello operator, {operator.fullname}")


@operator_router.callback_query(F.data.startswith("answer"))
async def answer_to_message(
    call: CallbackQuery, repo: "RequestsRepo", state: FSMContext
):
    await call.answer()

    text = call.message.text.split(":")[-1].replace("\n", "")
    print(call.from_user.username)
    operator = await repo.operators.get_operator_by_telegram_username(
        telegram_username=call.from_user.username
    )

    _, user_id = call.data.split(":")

    room = await repo.support_room.get_room(
        user_id=int(user_id),
        operator_id=operator.id,
    )

    if not room:
        room = await repo.support_room.create_room(
            user_id=int(user_id), operator_id=operator.id
        )
        print("room was created")

    # await repo.support_messages.create_message(message=text, room_id=room.id)

    await state.set_state(OperatorState.message)
    await state.update_data(room_id=room.id, operator_id=operator.id)
    await call.message.answer(text="Напишите ответ")


@operator_router.message(OperatorState.message)
async def answer_to_message(message: Message, repo: "RequestsRepo", state: FSMContext):
    cache = get_redis()

    data = await state.get_data()
    room_id = data.get("room_id")
    print(room_id)
    operator_id = data.get("operator_id")

    cached_room = cache.get(f"room:{room_id}")
    print(cached_room)
    new_message = await repo.support_messages.create_message(
        message=message.text,
        room_id=room_id,
        sender_id=operator_id,
    )
    new_message = SupportMessage.model_validate(new_message, from_attributes=True)
    if cached_room:
        cached_room = json.loads(cached_room)
        cached_room["messages"].append(new_message.model_dump())
        cache.set(f"room:{room_id}", json.dumps(cached_room))

    await message.answer("Ваш ответ был отправлен")
