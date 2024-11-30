import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.setup import create_engine, create_session_pool
from config.loader import load_config
from infrastructure.database.models import Place

from external.json.reader import get_test_places


async def add_mock_places(session: AsyncSession):
    test_places_json = get_test_places("external/data/places.json")

    places = []

    for obj in test_places_json:
        try:
            place = Place(
                name=obj["name"],
                category=obj["category"],
                address=obj["address"],
                coordinates=obj["coordinates"],
                phone_number=obj["phone­_number"],
                yandex_map_link=obj["yandex_map_link"],
                has_gasoline=obj["gasoline"],
                has_ai_80=obj["ai-80"],
                has_ai_91=obj["ai-91"],
                has_ai_95=obj["ai-92"],
                has_ai_98=obj["ai-95"],
                has_diesel=obj["ai-98"],
                working_hours=obj["working_hours"],
                has_wc=obj["wc"],
                has_wifi=obj["wifi"],
                has_shop=obj["shop"],
                has_parking=obj["parking"],
                has_car_wash=obj["car_wash"],
                has_tire_service=obj["tire_service"],
                has_gas=obj["gas"],
                has_methane=obj["methane"],
                has_propane=obj["propane"],
                has_praying_room=obj["praying_room"],
                has_electric_charging=obj["electric_charging"],
                user_id=1,
            )
            print(obj["name"])
            places.append(place)
        except Exception as e:
            continue
    session.add_all(places)
    await session.commit()


async def main():
    config = load_config(".env")
    engine = create_engine(config.db)
    session_pool = create_session_pool(engine)
    print("sadfsa")
    async with session_pool() as session:
        await add_mock_places(session)


if __name__ == "__main__":
    asyncio.run(main())
