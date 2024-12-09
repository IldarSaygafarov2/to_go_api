from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from infrastructure.database.models.fuel import FuelType


class FuelCreateDTO(BaseModel):
    fuel_type: FuelType
    price: int


class FuelDTO(BaseModel):
    id: int
    fuel_type: Optional[FuelType]
    place_id: int
    price: int
    created_at: datetime
