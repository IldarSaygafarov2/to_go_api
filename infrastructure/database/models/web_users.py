from typing import Optional
from sqlalchemy import JSON, false
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, created_at
from .mixins.int_id_pk import IntIdPkMixin


class WebUser(Base, IntIdPkMixin):
    username: Mapped[str]
    password: Mapped[str]
    hashed_password: Mapped[str]
    created_at: Mapped[created_at]
    scope: Mapped[Optional[dict]] = mapped_column(JSON, default=["authenticated"])
    is_superuser: Mapped[bool] = mapped_column(default=false())
    is_operator: Mapped[bool] = mapped_column(default=false())
