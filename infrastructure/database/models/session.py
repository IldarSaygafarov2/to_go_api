from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at
from .mixins.int_id_pk import IntIdPkMixin


class Session(Base, IntIdPkMixin):
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[created_at]
    expired_at: Mapped[created_at]
