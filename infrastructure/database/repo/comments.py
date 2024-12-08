from .base import BaseRepo

from sqlalchemy import insert, update, select, delete
from sqlalchemy.orm import selectinload

from infrastructure.database.models.place import PlaceComment


class PlaceCommentRepo(BaseRepo):
    async def add_comment(self, place_id: int, user_id: int, text: str):
        stmt = (
            insert(PlaceComment)
            .values(
                place_id=place_id,
                user_id=user_id,
                text=text,
            )
            .options(selectinload(PlaceComment.user))
            .returning(PlaceComment)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_place_comments(self, place_id: int):
        stmt = (
            select(PlaceComment)
            .where(PlaceComment.place_id == place_id)
            .options(selectinload(PlaceComment.user))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_comment(self, comment_id: int):
        stmt = delete(PlaceComment).where(PlaceComment.id == comment_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_comment(self, comment_id: int, text: str):
        stmt = (
            update(PlaceComment).values(text=text).where(PlaceComment.id == comment_id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
