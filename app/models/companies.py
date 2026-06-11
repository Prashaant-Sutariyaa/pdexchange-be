from sqlalchemy import (
    Column,
    String,
    Integer,
    SmallInteger,
    Date,
    Text,
)
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.base import ExchangeBase


class Company(ExchangeBase):
    __tablename__ = "companies"

    id = Column(String(12), primary_key=True)

    parent_id = Column(String(36))

    name = Column(String(200), nullable=False)
    li_name = Column(String(200))

    website = Column(String(250), nullable=False)
    email_domain = Column(String(250))

    phone = Column(String(20))
    alternate_phone = Column(String(20))

    li_industry_mapping_id = Column(SmallInteger)
    li_industry = Column(String(150))

    company_size = Column(String(50))
    emp_count = Column(Integer)

    revenue_range = Column(String(50))
    revenue = Column(String(30))

    type = Column(String(100))

    li_url = Column(String(250), nullable=False)
    revenue_url = Column(String(250))

    founded = Column(SmallInteger)

    global_hq = Column(String(250))

    comments = Column(Text)

    source = Column(String(50))
    source_id = Column(String(50), nullable=False)

    data_status = Column(String(50))

    linkedin_verified = Column(String(10))
    linkedin_verified_on = Column(Date)

    phone_verified = Column(String(10))
    phone_verified_on = Column(Date)

    db_refresh_valid = Column(SmallInteger)
    db_refreshed_on = Column(Date)

    status = Column(String(20))

    deleted = Column(SmallInteger, default=0)

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