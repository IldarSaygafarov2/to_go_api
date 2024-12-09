from sqlalchemy import select, exists, func
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models.place import PlaceRating

from .base import BaseRepo


class PlaceRatingRepo(BaseRepo):
    async def add_rating(self, place_id: int, user_id: int, rating: int):
        vote_exists = select(
            exists().where(
                PlaceRating.place_id == place_id,
                PlaceRating.user_id == user_id,
            )
        )
        vote_exists = await self.session.execute(vote_exists)
        if not vote_exists.scalar_one():
            stmt = (
                insert(PlaceRating)
                .values(place_id=place_id, user_id=user_id, rating=rating)
                .returning(PlaceRating)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()

    async def get_place_rating(self, place_id: int):
        stmt = select(
            func.sum(PlaceRating.rating),
            func.count(PlaceRating.id),
        ).where(PlaceRating.place_id == place_id)

        result = await self.session.execute(stmt)
        return result.fetchone()
