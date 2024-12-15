from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base, created_at
from .mixins.int_id_pk import IntIdPkMixin

# created_by_email
# created_by_name
# phone_number


class UserVerificationCode(Base, IntIdPkMixin):
    phone_number: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str]


class User(Base, IntIdPkMixin):
    fullname: Mapped[str] = mapped_column(nullable=True)
    user_photo: Mapped[Optional[str]]
    email: Mapped[Optional[str]]

    phone_number: Mapped[str]
    created_at: Mapped[created_at]

    comments = relationship("PlaceComment", back_populates="user")
    sent_messages = relationship(
        "Message",
        back_populates="sender",
        # foreign_keys=["messages.sender_id"],
    )
