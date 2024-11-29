from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, mapped_column

from infrastructure.utils import camel_case_to_snake_case

created_at = Annotated[datetime, mapped_column(TIMESTAMP, server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(TIMESTAMP, default=func.now(), onupdate=func.now())
]


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_case_to_snake_case(cls.__name__)
