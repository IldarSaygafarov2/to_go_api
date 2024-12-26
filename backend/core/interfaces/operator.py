from typing import Optional
from pydantic import BaseModel


class OperatorDTO(BaseModel):
    id: int
    fullname: str
    telegram_username: str
    telegram_chat_id: Optional[int]


class OperatorCreateDTO(BaseModel):
    fullname: str
    telegram_username: str


class OperatorEditDTO(BaseModel):
    fullname: str
    telegram_username: str
