import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from config.loader import load_config
from external.json.reader import load_json
from infrastructure.database.models import PlaceFuelPrice
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.setup import create_engine, create_session_pool


async def add_mock_places(session: AsyncSession):
    repo = RequestsRepo(session)
    places = await repo.places.get_all_places()

    test_places_json = load_json("external/data/fuel_prices.json")

    result = []
    for place in places:
        for obj in test_places_json:
            if place.row_id == obj["stationID"]:
                print(obj["fuel_type"])
                if not obj["fuel_type"]:
                    continue
                item = PlaceFuelPrice(
                    fuel_type=obj["fuel_type"],
                    place_id=place.id,
                    price=obj["price"] if obj["price"] else 0,
                )
                result.append(item)

    session.add_all(result)
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
