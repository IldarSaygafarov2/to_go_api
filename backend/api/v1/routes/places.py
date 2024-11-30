from fastapi import APIRouter, Depends
from backend.app.config import config
from backend.app.dependencies import get_repo
from infrastructure.database.repo.requests import RequestsRepo
from backend.core.interfaces.place import (
    PlaceDetailDTO,
    PlaceListDTO,
    PaginatedPlacesDTO,
)
from typing import Annotated


router = APIRouter(
    prefix=config.api_prefix.v1.places,
    tags=["Places"],
)


@router.get("/")
async def get_places(
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    offset: int = 1,
    limit: int = 14,
) -> PaginatedPlacesDTO:
    places = await repo.places.get_places(offset=offset, limit=limit)
    places = [
        PlaceListDTO.model_validate(place, from_attributes=True) for place in places
    ]
    total_places = await repo.places.get_total_places()
    return PaginatedPlacesDTO(
        total=total_places,
        limit=limit,
        offset=offset,
        places=places,
    )


@router.get("/{place_id}")
async def get_place_detail(
    place_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
) -> PlaceDetailDTO:
    place = await repo.places.get_place(place_id=place_id)
    return PlaceDetailDTO.model_validate(place, from_attributes=True)
