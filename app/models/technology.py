from sqlalchemy import (
    Column,
    String,
    Integer,
    SmallInteger,
    Numeric,
    Text,
)
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.base import ExchangeBase


class Technology(ExchangeBase):
    __tablename__ = "technology"

    id = Column(String(36), primary_key=True)

    name = Column(String(100), nullable=False)

    category_id = Column(String(36), nullable=False)

    url_slug = Column(String(100), nullable=False)

    description = Column(Text)

    meta_keyword = Column(Text)

    meta_description = Column(Text)

    meta_title = Column(String(200))

    page_header = Column(String(200))

    contact_price = Column(
        Numeric(6, 3),
        nullable=False,
        default=0,
    )

    company_price = Column(
        Numeric(6, 3),
        nullable=False,
        default=0,
    )

    created_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    modified_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    created_by = Column(
        Integer,
        default=1,
        nullable=False,
    )

    modified_by = Column(
        Integer,
        default=1,
        nullable=False,
    )

    status = Column(
        String(30),
        nullable=False,
    )

    deleted = Column(
        SmallInteger,
        default=0,
        nullable=False,
    )