from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SupportMessageCreateDTO(BaseModel):
    message: str


class SupportMessage(BaseModel):
    id: int
    message: str
    # created_at: datetime
    # updated_at: datetime


class SupportRoomDTO(BaseModel):
    id: int
    user_id: int
    operator_id: int
    messages: Optional[list[SupportMessage]]
