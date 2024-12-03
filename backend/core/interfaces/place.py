from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from backend.core.interfaces.fuel import FuelDTO


class PlaceListDTO(BaseModel):
    id: int
    name: str
    category: str
    working_hours: Optional[str]
    address: Optional[str]
    fuel_price: Optional[list[FuelDTO]]


class PlaceDetailDTO(BaseModel):
    id: int
    name: str
    category: str
    coordinates: str
    phone_number: str
    yandex_map_link: str
    fuel_price: Optional[list[FuelDTO]]
    created_at: datetime


class PaginatedPlacesDTO(BaseModel):
    total: int
    limit: int
    offset: int
    places: list[PlaceListDTO]
