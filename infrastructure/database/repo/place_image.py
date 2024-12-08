from sqlalchemy import insert

from infrastructure.database.models.place import PlaceImage

from .base import BaseRepo


class PlaceImageRepo(BaseRepo):
    async def insert_place_image(self, place_id: int, url: str):
        stmt = (
            insert(PlaceImage).values(place_id=place_id, url=url).returning(PlaceImage)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
