from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .place import PlaceRepo
from .user import UserRepo, UserVerificationCodeRepo
from .fuel import FuelRepo


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

    @property
    def fuel(self) -> FuelRepo:
        return FuelRepo(self.session)
