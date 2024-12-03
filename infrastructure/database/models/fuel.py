import enum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, created_at
from .mixins.int_id_pk import IntIdPkMixin


class FuelType(str, enum.Enum):
    diesel = "Дизель"
    methan = "Метан"
    propane = "Пропан"
    ai_80 = "АИ-80"
    ai_91 = "АИ-91"
    ai_92 = "АИ-92"
    ai_95 = "АИ-95"
    ai_98 = "АИ-98"


class PlaceFuelPrice(Base, IntIdPkMixin):
    fuel_type: Mapped[FuelType] = mapped_column(
        psql.ENUM(FuelType),
        nullable=True,
    )

    place_id: Mapped[int] = mapped_column(ForeignKey("places.id"))
    place = relationship("Place", back_populates="fuel_price")
    price: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[created_at]
