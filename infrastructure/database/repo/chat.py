from .base import BaseRepo

from sqlalchemy import insert, update, select, exists


from infrastructure.database.models import Chat, ChatMessage


class ChatRepo(BaseRepo):
    async def create_chat(self, sender_id: int, recipient_id: int):
        chat_exists = select(
            exists().where(
                Chat.sender_id == sender_id,
                Chat.recipient_id == recipient_id,
            )
        )
        chat_exists = await self.session.execute(chat_exists)
        if not chat_exists.scalar_one():
            stmt = (
                insert(Chat)
                .values(sender_id=sender_id, recipient_id=recipient_id)
                .returning(Chat)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one()


class ChatMessageRepo(BaseRepo):
    pass
