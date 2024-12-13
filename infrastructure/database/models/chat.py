from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, created_at, updated_at
from .mixins.int_id_pk import IntIdPkMixin


class Chat(Base, IntIdPkMixin):
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    recipient_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    created_at: Mapped[created_at]

    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="chat")


class ChatMessage(Base, IntIdPkMixin):
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"))

    content: Mapped[str]
    delivered_at: Mapped[updated_at]

    chat = relationship("Chat", back_populates="messages")
