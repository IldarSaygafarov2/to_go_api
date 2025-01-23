import enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects import postgresql as psql

from .base import Base, created_at, updated_at
from .mixins.int_id_pk import IntIdPkMixin


class ChatTypeEnum(str, enum.Enum):
    GLOBAL = "global"
    LOCAL = "local"


class GlobalChat(Base, IntIdPkMixin):
    created_at: Mapped[created_at]

    messages = relationship("Message", back_populates="chat")
    # participants = relationship("GlobalChat", back_populates="chat")


class GlobalChatParticipant(Base, IntIdPkMixin):
    chat_id: Mapped[int] = mapped_column(ForeignKey("global_chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    joined_at: Mapped[created_at]

    # chat = relationship(
    #     "GlobalChat", back_populates="participants", foreign_keys=[chat_id]
    # )
    # user = relationship("User", back_populates="participation_chats")


class PrivateChat(Base, IntIdPkMixin):
    user_id_1: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_id_2: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[created_at]

    user_1 = relationship("User", foreign_keys=[user_id_1])
    user_2 = relationship("User", foreign_keys=[user_id_2])

    messages = relationship("Message", back_populates="private_chat")


class Message(Base, IntIdPkMixin):
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("global_chats.id"), nullable=True)
    private_chat_id: Mapped[int] = mapped_column(
        ForeignKey("private_chats.id"), nullable=True
    )
    content: Mapped[str] = mapped_column(nullable=True)
    bytes_data: Mapped[bytes] = mapped_column(nullable=True)
    created_at: Mapped[created_at]

    sender = relationship(
        "User",
        back_populates="sent_messages",
        foreign_keys=[sender_id],
    )
    chat = relationship("GlobalChat", back_populates="messages", foreign_keys=[chat_id])
    private_chat = relationship("PrivateChat", back_populates="messages")

    @property
    def is_private(self):
        return self.private_chat is not None
