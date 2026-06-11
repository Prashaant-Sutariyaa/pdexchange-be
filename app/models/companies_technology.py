from sqlalchemy import (
    Column,
    String,
    Integer,
    SmallInteger,
)
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.base import ExchangeBase


class CompanyTechnology(ExchangeBase):
    __tablename__ = "companies_technology"

    id = Column(
        String(36),
        primary_key=True,
    )

    company_id = Column(String(12))

    technology_id = Column(String(36))

    created_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    modified_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    created_by = Column(Integer)

    modified_by = Column(Integer)

    status = Column(String(30))

    deleted = Column(
        SmallInteger,
        default=0,
    )
