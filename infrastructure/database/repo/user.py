from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User, UserVerificationCode

from .base import BaseRepo


class UserRepo(BaseRepo):
    async def insert_user(
        self,
        phone_number: str,
    ):
        stmt = insert(User).values(phone_number=phone_number).returning(User)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_user_by_phone_number(self, phone_number: str):
        stmt = select(User).where(User.phone_number == phone_number)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, fullname: str, user_photo: str):
        stmt = (
            update(User)
            .values(fullname=fullname, user_photo=user_photo)
            .where(User.id == user_id)
            .returning(User)
        )
        updated = await self.session.execute(stmt)
        await self.session.commit()
        return updated.scalar_one()

    async def get_total_users(self):
        stmt = select(func.count(User.id))
        result = await self.session.execute(stmt)
        return result.scalar_one()


class UserVerificationCodeRepo(BaseRepo):
    async def is_code_exists(self, phone_number: str, code: str):
        stmt = select(UserVerificationCode).where(
            UserVerificationCode.phone_number == phone_number,
            UserVerificationCode.code == code,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def insert_verification_code(self, phone_number: str, code: str):
        stmt = (
            insert(UserVerificationCode)
            .values(phone_number=phone_number, code=code)
            .on_conflict_do_update(
                index_elements=["phone_number"],
                set_=dict(code=code),
            )
            .returning(UserVerificationCode)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
