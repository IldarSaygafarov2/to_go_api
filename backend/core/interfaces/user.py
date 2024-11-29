from pydantic import BaseModel


class LoginUserDTO(BaseModel):
    phone_number: str


class UserRegistrationDTO(BaseModel):
    phone_number: str


class UserAuthDTO(BaseModel):
    phone_number: str
    code: str
