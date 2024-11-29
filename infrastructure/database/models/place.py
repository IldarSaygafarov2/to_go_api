from .base import Base, created_at
from .mixins.int_id_pk import IntIdPkMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import false, ForeignKey


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

    created_at: Mapped[created_at]


# name
# category
# address
# coordinates
# phone_number
# yandex_map_link
# gasoline
# ai-80
# ai-91
# ai-95
# ai-98
# diesel
# working_hours
# wc
# shop
# cafe
# parking
# car_wash
# tire_service

# creation_date
# gas
# methane
# propane
# praying_room
# electric_charging
