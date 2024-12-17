from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, File, UploadFile

from backend.app.config import config
from backend.app.dependencies import get_repo
from backend.core.interfaces.fuel import FuelCreateDTO, FuelDTO
from backend.core.interfaces.place import (
    PaginatedPlacesDTO,
    PlaceCommentCreateDTO,
    PlaceCommentDTO,
    PlaceCreateDTO,
    PlaceDetailDTO,
    PlaceRatingCreateDTO,
    PlaceRatingDTO,
    PlaceNameCoordinateDTO,
)
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.utils.helpers import create_images_dir

router = APIRouter(
    prefix=config.api_prefix.v1.places,
    tags=["Places"],
)


@router.post("/create")
async def create_place(
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    place_data: PlaceCreateDTO = Body(...),
    images: Optional[list[UploadFile]] = File(),
):

    data = place_data.model_dump()
    place = await repo.places.insert_place(**data)

    images_dir = create_images_dir(f"places/{place.row_id}/")
    for image in images:
        filename = image.filename
        path = images_dir / filename
        with open(path, "wb") as f:
            f.write(await image.read())
        await repo.place_images.insert_place_image(place_id=place.id, url=str(path))

    new_place = await repo.places.get_place(place_id=place.id)
    return PlaceDetailDTO.model_validate(new_place, from_attributes=True)


@router.get("/")
async def get_places(
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    offset: int = 1,
    limit: int = 14,
) -> PaginatedPlacesDTO:

    places = []

    db_places = await repo.places.get_places(offset=offset, limit=limit)
    for place in db_places:
        rating, count = await repo.place_rating.get_place_rating(place_id=place.id)
        if rating is not None and count:
            _rating = rating / count
        else:
            _rating = 0

        places.append(
            {
                "id": place.id,
                "name": place.name,
                "category": place.category,
                "address": place.address,
                "coordinates": place.coordinates,
                "working_hours": place.working_hours,
                "rating": _rating,
                "reviews_count": count,
                "fuel_price": place.fuel_price,
            }
        )

    total_places = await repo.places.get_total_places()

    result = {
        "total": total_places,
        "limit": limit,
        "offset": offset,
        "places": places,
    }
    return result


@router.get("/all")
async def get_all_places_names_and_coordinates(
    repo: Annotated[RequestsRepo, Depends(get_repo)],
) -> list[PlaceNameCoordinateDTO]:
    places = await repo.places.get_all_places()
    return [
        PlaceNameCoordinateDTO.model_validate(place, from_attributes=True)
        for place in places
    ]


@router.get("/{place_id}")
async def get_place_detail(
    place_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
) -> PlaceDetailDTO:
    place = await repo.places.get_place(place_id=place_id)
    return PlaceDetailDTO.model_validate(place, from_attributes=True)


@router.post("/{place_id}/comments/create")
async def create_place_comment(
    place_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    comment_data: PlaceCommentCreateDTO,
):
    comment = await repo.place_comments.add_comment(
        place_id=place_id,
        user_id=comment_data.user_id,
        text=comment_data.text,
    )
    return PlaceCommentDTO.model_validate(comment, from_attributes=True)


@router.post("/{place_id}/fuel/create")
async def create_place_fuel_type(
    place_id: int,
    fuel_data: FuelCreateDTO,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
) -> FuelDTO:
    new_fuel = await repo.fuel.insert_fuel_price(
        fuel_type=fuel_data.fuel_type,
        place_id=place_id,
        price=fuel_data.price,
    )
    return FuelDTO.model_validate(new_fuel, from_attributes=True)


@router.post("/{place_id}/rating/add/")
async def add_rating_to_place(
    place_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    place_rating_data: PlaceRatingCreateDTO,
):
    rating = await repo.place_rating.add_rating(
        place_id=place_id,
        user_id=place_rating_data.user_id,
        rating=place_rating_data.rating,
    )
    if rating is None:
        return {"detail": "vote already added"}
    return PlaceRatingDTO.model_validate(rating, from_attributes=True)
