from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .comments import PlaceCommentRepo
from .fuel import FuelRepo
from .place import PlaceRepo
from .place_image import PlaceImageRepo
from .place_rating import PlaceRatingRepo
from .user import UserRepo, UserVerificationCodeRepo
from .chat import ChatMessageRepo, PrivateChatRepo


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

    @property
    def place_rating(self) -> PlaceRatingRepo:
        return PlaceRatingRepo(self.session)

    @property
    def chat_messages(self) -> ChatMessageRepo:
        return ChatMessageRepo(self.session)

    @property
    def private_chats(self) -> PrivateChatRepo:
        return PrivateChatRepo(self.session)
