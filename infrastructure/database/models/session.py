from datetime import datetime

from .base import Base, created_at

from sqlalchemy.orm import Mapped, mapped_column
from .mixins.int_id_pk import IntIdPkMixin
from sqlalchemy import String

class Session(Base, IntIdPkMixin):
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[created_at]
    expired_at: Mapped[created_at]

