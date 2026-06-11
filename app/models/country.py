from sqlalchemy import (
    Column,
    BigInteger,
    String,
)
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.base import ExchangeBase


class Country(ExchangeBase):
    __tablename__ = "countries"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    region = Column(
        String(100),
        nullable=False,
    )

    iso3 = Column(
        String(3),
        nullable=True,
    )

    iso2 = Column(
        String(2),
        nullable=True,
    )

    phonecode = Column(
        String(20),
        nullable=True,
    )

    capital = Column(
        String(255),
        nullable=True,
    )

    currency = Column(
        String(255),
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
        default="Active",
    )

    wikidata_id = Column(
        String(255),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
