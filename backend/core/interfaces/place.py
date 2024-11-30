from pydantic import BaseModel
from datetime import datetime


class PlaceListDTO(BaseModel):
    id: int
    name: str
    category: str


class PlaceDetailDTO(BaseModel):
    id: int
    name: str
    category: str
    coordinates: str
    phone_number: str
    yandex_map_link: str
    created_at: datetime


class PaginatedPlacesDTO(BaseModel):
    total: int
    limit: int
    offset: int
    places: list[PlaceListDTO]
