from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .chat import ChatMessageRepo, PrivateChatRepo
from .comments import PlaceCommentRepo
from .fuel import FuelRepo
from .place import PlaceRepo
from .place_image import PlaceImageRepo
from .place_rating import PlaceRatingRepo
from .support import OperatorRepo, SupportMessageRepo, SupportRoomRepo
from .user import UserRepo, UserVerificationCodeRepo


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

    @property
    def operators(self) -> OperatorRepo:
        return OperatorRepo(self.session)

    @property
    def support_messages(self) -> SupportMessageRepo:
        return SupportMessageRepo(self.session)

    @property
    def support_room(self) -> SupportRoomRepo:
        return SupportRoomRepo(self.session)
