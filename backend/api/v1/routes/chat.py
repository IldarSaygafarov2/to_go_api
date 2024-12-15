from typing import Annotated
from fastapi import APIRouter, Depends
from backend.app.config import config
from backend.app.dependencies import get_repo

from infrastructure.database.repo.requests import RequestsRepo


router = APIRouter(
    prefix=config.api_prefix.v1.chat,
    tags=["Chat"],
)


@router.get("/global")
async def get_global_chat_messages(
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    messages = await repo.chat_messages.get_global_chat_messages()
    return messages


@router.get("/private/{sender_id}/{recipient_id}/")
async def get_private_chat(
    sender_id: int,
    recipient_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    chat = await repo.private_chats.get_chat(
        sender_id=sender_id, recipient_id=recipient_id
    )
    return chat
