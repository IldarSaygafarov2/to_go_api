from typing import Optional

from pydantic import BaseModel, Field


class PlaceFilter(BaseModel):
    has_gasoline: Optional[bool] = Field(None)
    has_ai_80: Optional[bool] = Field(None)
    has_ai_91: Optional[bool] = Field(None)
    has_ai_95: Optional[bool] = Field(None)
    has_ai_98: Optional[bool] = Field(None)
    has_diesel: Optional[bool] = Field(None)
    name: Optional[str] = Field(None)
    limit: int = Field(14)
    offset: int = Field(0)
