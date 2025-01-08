from sqlalchemy import ForeignKey, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, created_at, updated_at
from .mixins.int_id_pk import IntIdPkMixin


class Operator(Base, IntIdPkMixin):
    fullname: Mapped[str]
    telegram_username: Mapped[str] = mapped_column(unique=True)
    telegram_chat_id = mapped_column(BIGINT, nullable=True)


class SupportRoom(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"))
    created_at: Mapped[created_at]

    messages: Mapped[list["SupportMessage"]] = relationship(back_populates="room")
    sender = relationship("User", back_populates="support_room")


class SupportMessage(Base, IntIdPkMixin):
    message: Mapped[str]
    room_id: Mapped[int] = mapped_column(ForeignKey("support_rooms.id"))
    sender_id: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    room = relationship("SupportRoom", back_populates="messages")

    # sender: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # is_answered: Mapped[bool] = mapped_column(default=False)
    # answered_by: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=True)
