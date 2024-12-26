from sqlalchemy import false
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, created_at
from .mixins.int_id_pk import IntIdPkMixin


class WebUser(Base, IntIdPkMixin):
    username: Mapped[str]
    password: Mapped[str]
    hashed_password: Mapped[str]
    created_at: Mapped[created_at]
    is_superuser: Mapped[bool] = mapped_column(default=false())
    is_operator: Mapped[bool] = mapped_column(default=false())
