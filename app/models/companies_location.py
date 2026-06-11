from sqlalchemy import (
    Column,
    String,
    SmallInteger,
    Date,
)
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.base import ExchangeBase


class CompanyLocation(ExchangeBase):
    __tablename__ = "companies_location"

    id = Column(String(12), primary_key=True)

    company_id = Column(String(12))

    name = Column(String(200), nullable=False)
    li_name = Column(String(200))

    website = Column(String(250), nullable=False)

    address1 = Column(String(250))
    address2 = Column(String(250))

    city = Column(String(100))
    state = Column(String(100))

    zip_code = Column(String(10))

    country = Column(String(100), nullable=False)

    li_url = Column(String(250), nullable=False)

    email_topology = Column(String(15))
    email_domain = Column(String(250))
    email_pattern_source = Column(String(10))

    phone = Column(String(20))
    alternate_phone = Column(String(20))

    db_refresh_valid = Column(SmallInteger)
    db_refreshed_on = Column(Date)

    source = Column(String(50))

    created_by = Column(SmallInteger)
    modified_by = Column(SmallInteger)

    created_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    modified_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )