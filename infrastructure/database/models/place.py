import enum
from sqlalchemy import ForeignKey, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects import postgresql as psql

from .base import Base, created_at
from .mixins.int_id_pk import IntIdPkMixin


class PlaceRatingEnum(int, enum.Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class Place(Base, IntIdPkMixin):
    name: Mapped[str]
    category: Mapped[str]
    address: Mapped[str]
    coordinates: Mapped[str]
    phone_number: Mapped[str] = mapped_column(nullable=True)
    yandex_map_link: Mapped[str] = mapped_column(nullable=True)
    has_gasoline: Mapped[bool] = mapped_column(default=false())
    has_ai_80: Mapped[bool] = mapped_column(default=false())
    has_ai_91: Mapped[bool] = mapped_column(default=false())
    has_ai_95: Mapped[bool] = mapped_column(default=false())
    has_ai_98: Mapped[bool] = mapped_column(default=false())
    has_diesel: Mapped[bool] = mapped_column(default=false())
    working_hours: Mapped[str] = mapped_column(nullable=True)
    has_wc: Mapped[bool] = mapped_column(default=false())
    has_wifi: Mapped[bool] = mapped_column(default=false())
    has_shop: Mapped[bool] = mapped_column(default=false())
    has_parking: Mapped[bool] = mapped_column(default=false())
    has_car_wash: Mapped[bool] = mapped_column(default=false())
    has_tire_service: Mapped[bool] = mapped_column(default=false())
    has_gas: Mapped[bool] = mapped_column(default=false())
    has_methane: Mapped[bool] = mapped_column(default=false())
    has_propane: Mapped[bool] = mapped_column(default=false())
    has_praying_room: Mapped[bool] = mapped_column(default=false())
    has_electric_charging: Mapped[bool] = mapped_column(default=false())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    fuel_price = relationship("PlaceFuelPrice", back_populates="place")

    images: Mapped[list["PlaceImage"]] = relationship(back_populates="place")
    comments: Mapped[list["PlaceComment"]] = relationship(back_populates="place")
    rating: Mapped["PlaceRating"] = relationship(back_populates="place")

    created_at: Mapped[created_at]


class PlaceComment(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    place_id: Mapped[int] = mapped_column(ForeignKey("places.id", ondelete="CASCADE"))
    text: Mapped[str]
    created_at: Mapped[created_at]

    place = relationship("Place", back_populates="comments")
    user = relationship("User", back_populates="comments")


class PlaceImage(Base, IntIdPkMixin):
    place_id: Mapped[int] = mapped_column(ForeignKey("places.id", ondelete="CASCADE"))
    url: Mapped[str]

    place = relationship("Place", back_populates="images")


class PlaceRating(Base, IntIdPkMixin):
    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    rating: Mapped[int]

    place = relationship("Place", back_populates="rating")
