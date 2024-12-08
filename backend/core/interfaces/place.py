import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator

from backend.core.interfaces.fuel import FuelDTO
from backend.core.interfaces.user import UserProfileDTO


class PlaceListDTO(BaseModel):
    id: int
    name: str
    category: str
    working_hours: Optional[str]
    address: Optional[str]
    coordinates: Optional[str]
    fuel_price: Optional[list[FuelDTO]]


class PlaceImageDTO(BaseModel):
    id: int
    url: str


class PlaceCommentDTO(BaseModel):
    id: int
    text: str
    created_at: datetime
    user: UserProfileDTO


class PlaceCommentCreateDTO(BaseModel):
    user_id: int
    text: str


class PlaceDetailDTO(BaseModel):
    id: int
    name: str
    category: str
    coordinates: str
    phone_number: str
    yandex_map_link: str
    created_at: datetime
    fuel_price: Optional[list[FuelDTO]]
    images: Optional[list[PlaceImageDTO]]
    comments: Optional[list[PlaceCommentDTO]]


class PlaceImageDTO(BaseModel):
    id: int
    url: str


class PlaceCreateDTO(BaseModel):
    name: str
    address: str
    category: str
    working_hours: Optional[str]
    user_id: int
    has_gasoline: bool = False
    has_ai_80: bool = False
    has_ai_91: bool = False
    has_ai_95: bool = False
    has_ai_98: bool = False
    has_methane: bool = False
    has_propane: bool = False
    has_electric_charging: Optional[bool] = False
    has_wc: Optional[bool] = False
    has_shop: Optional[bool] = False
    has_car_wash: Optional[bool] = False

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class PaginatedPlacesDTO(BaseModel):
    total: int
    limit: int
    offset: int
    places: list[PlaceListDTO]
