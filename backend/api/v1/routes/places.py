from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.config import config
from backend.app.dependencies import get_repo
from backend.core.interfaces.place import (
    PaginatedPlacesDTO,
    PlaceDetailDTO,
    PlaceListDTO,
)
from infrastructure.database.repo.requests import RequestsRepo
from backend.core.interfaces.fuel import FuelCreateDTO, FuelDTO

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
