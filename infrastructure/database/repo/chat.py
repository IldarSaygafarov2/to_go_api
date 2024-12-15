from sqlalchemy import exists, insert, select
from sqlalchemy.orm import selectinload

from infrastructure.database.models.chat import (
    GlobalChat,
    GlobalChatParticipant,
    Message,
    PrivateChat,
)

from .base import BaseRepo


class ChatMessageRepo(BaseRepo):
    async def add_global_message(self, sender_id: int, content: str):
        stmt = insert(Message).values(sender_id=sender_id, content=content, chat_id=1)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_global_chat_messages(self, chat_id: int = 1):
        stmt = (
            select(Message)
            .options(selectinload(Message.sender))
            .where(Message.chat_id == chat_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_private_message(
        self, sender_id: int, content: str, private_chat_id: int
    ):
        stmt = insert(Message).values(
            sender_id=sender_id,
            chat_id=None,
            private_chat_id=private_chat_id,
            content=content,
        )
        await self.session.execute(stmt)
        await self.session.commit()


class PrivateChatRepo(BaseRepo):
    async def create_chat_if_not_exists(self, sender_id: int, recipient_id: int):
        chat_exists = select(PrivateChat).filter(
            (
                PrivateChat.user_id_1 == sender_id
                and PrivateChat.user_id_2 == recipient_id
            )
            | (
                PrivateChat.user_id_2 == sender_id
                and PrivateChat.user_id_1 == recipient_id
            )
        )
        chat_exists = await self.session.execute(chat_exists)

        if not chat_exists.first():
            stmt = (
                insert(PrivateChat)
                .values(user_id_1=sender_id, user_id_2=recipient_id)
                .returning(PrivateChat)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()

    async def get_chat(self, sender_id: int, recipient_id: int):
        stmt = (
            select(PrivateChat)
            .where(
                (
                    PrivateChat.user_id_1 == sender_id
                    and PrivateChat.user_id_2 == recipient_id
                )
                | (
                    PrivateChat.user_id_2 == sender_id
                    and PrivateChat.user_id_1 == recipient_id
                )
            )
            .options(
                selectinload(PrivateChat.messages),
                selectinload(PrivateChat.user_1),
                selectinload(PrivateChat.user_2),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
