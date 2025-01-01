import uuid

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

from infrastructure.database.models.place import Place, PlaceComment, PlaceRating

from .base import BaseRepo


class PlaceRepo(BaseRepo):

    async def insert_place(
        self,
        name: str,
        category: str,
        address: str,
        user_id: int,
        coordinates: str = "",
        phone_number: str = "",
        yandex_map_link: str = "",
        has_gasoline: bool = False,
        has_ai_80: bool = False,
        has_ai_91: bool = False,
        has_ai_95: bool = False,
        has_ai_98: bool = False,
        has_diesel: bool = False,
        working_hours: str = "",
        has_wc: bool = False,
        has_wifi: bool = False,
        has_shop: bool = False,
        has_parking: bool = False,
        has_car_wash: bool = False,
        has_tire_service: bool = False,
        has_gas: bool = False,
        has_methane: bool = False,
        has_propane: bool = False,
        has_praying_room: bool = False,
        has_electric_charging: bool = False,
    ):
        row_id = str(uuid.uuid4())
        stmt = (
            insert(Place)
            .values(
                row_id=row_id,
                name=name,
                category=category,
                address=address,
                coordinates=coordinates,
                phone_number=phone_number,
                yandex_map_link=yandex_map_link,
                has_gasoline=has_gasoline,
                has_ai_80=has_ai_80,
                has_ai_91=has_ai_91,
                has_ai_95=has_ai_95,
                has_ai_98=has_ai_98,
                has_diesel=has_diesel,
                working_hours=working_hours,
                has_wc=has_wc,
                has_wifi=has_wifi,
                has_shop=has_shop,
                has_parking=has_parking,
                has_car_wash=has_car_wash,
                has_tire_service=has_tire_service,
                has_gas=has_gas,
                has_methane=has_methane,
                has_propane=has_propane,
                has_praying_room=has_praying_room,
                has_electric_charging=has_electric_charging,
                user_id=user_id,
            )
            .returning(Place)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_places(self, offset: int, limit: int):
        stmt = (
            select(Place)
            .options(selectinload(Place.fuel_price))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_filtered_places(self, filters: dict):
        _stmt = select(Place).options(selectinload(Place.fuel_price))
        name_field = filters.get("name")
        if name_field is not None:
            filters.pop("name")
            stmt = _stmt.filter(Place.name.like(f"%{name_field}%")).filter_by(**filters)
        else:
            stmt = _stmt.filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_places(self):
        stmt = select(Place)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count_total_places(self):
        stmt = select(func.count(Place.id))
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_place(self, place_id: int):
        sub_stmt = select(func.avg(PlaceRating.rating)).where(PlaceRating.place_id == place_id).subquery()
        stmt = (
            select(Place, sub_stmt)
            .where(Place.id == place_id)
            .options(
                selectinload(Place.images),
                selectinload(Place.fuel_price),
                selectinload(Place.comments).subqueryload(PlaceComment.user),
                selectinload(Place.user)
            )
        )
        result = await self.session.execute(stmt)
        return result.fetchone()
