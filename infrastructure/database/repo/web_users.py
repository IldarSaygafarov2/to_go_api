from .base import BaseRepo

from sqlalchemy import insert, select

from infrastructure.database.models import WebUser


class WebUsersRepo(BaseRepo):
    async def insert_user(self):
        pass

    async def get_user(self, user_id: int):
        stmt = select(WebUser).where(WebUser.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username_and_password(self, username: str, password: str):
        stmt = (
            select(WebUser)
            .where(WebUser.username == username, WebUser.password == password)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
