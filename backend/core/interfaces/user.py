from typing import Optional
from pydantic import BaseModel
from fastapi import Body


class LoginUserDTO(BaseModel):
    phone_number: str


class UserRegistrationDTO(BaseModel):
    phone_number: str


class UserAuthDTO(BaseModel):
    phone_number: str
    code: str


class UserProfileDTO(BaseModel):
    id: int
    fullname: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    user_photo: Optional[str]


class UserProfileUpdateDTO(BaseModel):
    fullname: str = Body(...)
