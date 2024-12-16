import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession

from config.loader import load_config
from external.json.reader import get_test_places
from infrastructure.database.models.place import Place, PlaceImage
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.setup import create_engine, create_session_pool


async def add_mock_places(session: AsyncSession):
    repo = RequestsRepo(session)
    db_places = await repo.places.get_all_places()

    path = "media/places"

    places = []
    places_images_dir = os.listdir(path)

    for place in db_places:
        for _dir in places_images_dir:
            if place.row_id != _dir:
                continue

            for image in os.listdir(f"{path}/{_dir}"):
                await repo.place_images.insert_place_image(
                    place_id=place.id, url=f"{path}/{_dir}/{image}"
                )

                print(f"added {image} to {place.id}")

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
