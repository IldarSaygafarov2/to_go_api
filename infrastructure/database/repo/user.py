from .base import BaseRepo

from sqlalchemy import select
from infrastructure.database.models import User, UserVerificationCode
from sqlalchemy.dialects.postgresql import insert


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
