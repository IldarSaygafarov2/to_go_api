from .base import BaseRepo

from sqlalchemy import insert
from infrastructure.database.models import PlaceFuelPrice
from infrastructure.database.models.fuel import FuelType


class FuelRepo(BaseRepo):
    async def insert_fuel_price(self, fuel_type: str, place_id: int, price: int):
        stmt = (
            insert(PlaceFuelPrice)
            .values(
                fuel_type=fuel_type,
                place_id=place_id,
                price=price,
            )
            .returning(PlaceFuelPrice)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
