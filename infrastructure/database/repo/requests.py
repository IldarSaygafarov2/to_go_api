from dataclasses import dataclass

from .place import PlaceRepo
from .user import UserRepo, UserVerificationCodeRepo
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class RequestsRepo:
    session: AsyncSession

    @property
    def places(self) -> PlaceRepo:
        return PlaceRepo(self.session)

    @property
    def users(self) -> UserRepo:
        return UserRepo(self.session)

    @property
    def users_verification(self) -> UserVerificationCodeRepo:
        return UserVerificationCodeRepo(self.session)
