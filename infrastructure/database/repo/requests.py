from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .fuel import FuelRepo
from .place import PlaceRepo
from .place_image import PlaceImageRepo
from .user import UserRepo, UserVerificationCodeRepo
from .comments import PlaceCommentRepo


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

    @property
    def place_images(self) -> PlaceImageRepo:
        return PlaceImageRepo(self.session)

    @property
    def place_comments(self) -> PlaceCommentRepo:
        return PlaceCommentRepo(self.session)
