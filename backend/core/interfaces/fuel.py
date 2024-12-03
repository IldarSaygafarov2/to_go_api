from datetime import datetime

from pydantic import BaseModel

from infrastructure.database.models.fuel import FuelType


class FuelCreateDTO(BaseModel):
    fuel_type: FuelType
    price: int


class FuelDTO(BaseModel):
    id: int
    fuel_type: FuelType
    place_id: int
    price: int
    created_at: datetime
