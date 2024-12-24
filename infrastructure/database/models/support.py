from sqlalchemy import ForeignKey
from .base import Base, created_at, updated_at
from .mixins.int_id_pk import IntIdPkMixin

from sqlalchemy.orm import Mapped, mapped_column


class Operator(Base, IntIdPkMixin):
    fullname: Mapped[str]
    telegram_username: Mapped[str] = mapped_column(unique=True)
    telegram_chat_id: Mapped[int] = mapped_column(nullable=True)


class SupportMessage(Base, IntIdPkMixin):
    message: Mapped[str]
    sender: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_answered: Mapped[bool] = mapped_column(default=False)
    answered_by: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
