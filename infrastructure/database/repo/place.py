from .base import BaseRepo
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import Place


class PlaceRepo(BaseRepo):
    async def insert_place(
        self,
        name: str,
        category: str,
        address: str,
        coordinates: str,
        phone_number: str,
        yandex_map_link: str,
        has_gasoline: bool,
        has_ai_80: bool,
        has_ai_91: bool,
        has_ai_95: bool,
        has_ai_98: bool,
        has_diesel: bool,
        working_hours: str,
        has_wc: bool,
        has_wifi: bool,
        has_shop: bool,
        has_parking: bool,
        has_car_wash: bool,
        has_tire_service: bool,
        has_gas: bool,
        has_methane: bool,
        has_propane: bool,
        has_praying_room: bool,
        has_electric_charging: bool,
        user_id: int,
    ):
        stmt = (
            insert(Place)
            .values(
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
    
