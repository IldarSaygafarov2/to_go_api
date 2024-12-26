from .base import BaseRepo

from sqlalchemy import select


from infrastructure.database.models import Session


class SessionRepo(BaseRepo):
    async def get_session(self, user_id: int):
        stmt = (
            select(Session)
            .where(Session.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_session_by_token(self, token: str):
        stmt = select(Session).where(Session.token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()