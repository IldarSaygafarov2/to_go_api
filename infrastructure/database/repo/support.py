from typing import Optional

from sqlalchemy import delete, insert, select, update

from infrastructure.database.models.support import Operator, SupportMessage

from .base import BaseRepo


class OperatorRepo(BaseRepo):
    async def add_operator(
        self,
        fullname: str,
        telegram_username: str,
        telegram_chat_id: Optional[int] = None,
    ):
        stmt = (
            insert(Operator)
            .values(
                fullname=fullname,
                telegram_username=telegram_username,
                telegram_chat_id=telegram_chat_id,
            )
            .returning(Operator)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def update_telegram_chat_id(self, operator_id: int, telegram_chat_id: int):
        stmt = (
            update(Operator)
            .values(telegram_chat_id=telegram_chat_id)
            .where(Operator.id == operator_id)
            .returning(Operator)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_operator_by_telegram_username(self, telegram_username: str):
        stmt = select(Operator).where(Operator.telegram_username == telegram_username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_operators(self):
        stmt = select(Operator)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class SupportMessageRepo(BaseRepo):
    async def create_message(self, message: str, sender: int):
        stmt = (
            insert(SupportMessage)
            .values(message=message, sender=sender)
            .returning(SupportMessage)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def update_message(
        self, message_id: int, is_answered: bool, answered_by: int
    ):
        stmt = (
            update(SupportMessage)
            .values(is_answered=is_answered, answered_by=answered_by)
            .where(SupportMessage.id == message_id)
            .returning(SupportMessage)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
