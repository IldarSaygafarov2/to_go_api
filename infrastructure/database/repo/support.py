from typing import Optional

from sqlalchemy import delete, exists, insert, select, update
from sqlalchemy.orm import selectinload

from infrastructure.database.models.support import Operator, SupportMessage, SupportRoom

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

    async def update_operator(self, operator_id: int, **fields):
        stmt = (
            update(Operator)
            .where(Operator.id == operator_id)
            .values(**fields)
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

    async def get_operator_by_id(self, operator_id: int):
        stmt = select(Operator).where(Operator.id == operator_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class SupportRoomRepo(BaseRepo):
    async def get_room(self, user_id: int, operator_id: int):
        stmt = (
            select(SupportRoom)
            .where(
                SupportRoom.user_id == user_id, SupportRoom.operator_id == operator_id
            )
            .options(selectinload(SupportRoom.messages))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_support_rooms(self, operator_id: int):
        stmt = (
            select(SupportRoom)
            .where(SupportRoom.operator_id == operator_id)
            .options(
                selectinload(SupportRoom.messages),
                selectinload(SupportRoom.sender),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_rooms(self):
        stmt = select(SupportRoom).options(selectinload(SupportRoom.messages))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_room(self, user_id: int, operator_id: int):
        stmt = (
            insert(SupportRoom)
            .values(user_id=user_id, operator_id=operator_id)
            .returning(SupportRoom)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()


class SupportMessageRepo(BaseRepo):
    async def create_message(self, message: str, room_id: int, sender_id: int):
        stmt = (
            insert(SupportMessage)
            .values(
                message=message,
                room_id=room_id,
                sender_id=sender_id,
            )
            .returning(SupportMessage)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_room_messages(self, room_id: int):
        stmt = select(SupportMessage).where(SupportMessage.room_id == room_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
