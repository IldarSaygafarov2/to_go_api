from .base import BaseRepo

from sqlalchemy import delete, insert, select


from infrastructure.database.models import Session


class SessionRepo(BaseRepo):
    async def get_session(self, user_id: int):
        stmt = select(Session).where(Session.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_session_by_token(self, token: str):
        stmt = select(Session).where(Session.token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_session(self, token: str):
        stmt = delete(Session).where(Session.token == token)
        await self.session.execute(stmt)
        await self.session.commit()

    async def create_session(self, user_id: int, token: str, expire_at):
        stmt = (
            insert(Session)
            .values(token=token, user_id=user_id, expired_at=expire_at)
            .returning(Session)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
