import json
from typing import Annotated

from fastapi import APIRouter, Body, Depends
from redis import Redis

from backend.app.config import config
from backend.app.dependencies import get_redis, get_repo, get_telegram_service
from backend.core.interfaces.support import (
    SupportMessage,
    SupportMessageCreateDTO,
    SupportRoomDTO,
)
from infrastructure.database.repo.requests import RequestsRepo

router = APIRouter(
    prefix=config.api_prefix.v1.support,
    tags=["Support"],
)


telegram_service = get_telegram_service()


@router.get('/rooms/')
async def get_all_rooms(
        repo: Annotated[RequestsRepo, Depends(get_repo)]
):
    rooms = await repo.support_room.get_all_rooms()
    return rooms


@router.post("/{user_id}/send_message")
async def send_user_message_to_operators(
    user_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    cache: Annotated[Redis, Depends(get_redis)],
    message: SupportMessageCreateDTO = Body(...),
):
    user = await repo.users.get_user_by_id(user_id=user_id)

    operators = await repo.operators.get_all_operators()
    for operator in operators:
        room = await repo.support_room.get_room(
            user_id=user_id, operator_id=operator.id
        )

        if room is not None:
            new_message = await repo.support_messages.create_message(
                message=message.message,
                room_id=room.id,
                sender_id=user_id,
            )
            room_messages = cache.get(f"room:{room.id}")
            if room_messages:
                room_messages = json.loads(room_messages)
                new_message = SupportMessage.model_validate(
                    new_message, from_attributes=True
                )
                room_messages["messages"].append(new_message.model_dump())

                cache.set(f"room:{room.id}", json.dumps(room_messages))

        await telegram_service.send_message(
            telegram_chat_id=operator.telegram_chat_id,
            message=f"Message from <b>{user.fullname}</b>:\n\n" + message.message,
            user_id=user.id,
        )
    return {"is_sent": True}


@router.get("/{user_id}/{operator_id}/messages")
async def get_room_messages(
    user_id: int,
    operator_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    cache: Annotated[Redis, Depends(get_redis)],
):

    room = await repo.support_room.get_room(user_id=user_id, operator_id=operator_id)
    room = SupportRoomDTO.model_validate(room, from_attributes=True)

    in_cache = cache.get(f"room:{room.id}")
    if not in_cache:
        cache.set(f"room:{room.id}", json.dumps(room.model_dump(), ensure_ascii=False))

    return json.loads(in_cache) if in_cache else room


@router.get("/{room_id}/messages/")
async def get_room_messages_by_room_id(
    room_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    messages = await repo.support_messages.get_room_messages(room_id=room_id)
    return messages
