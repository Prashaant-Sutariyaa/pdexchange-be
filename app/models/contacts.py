from sqlalchemy import (
    Column,
    String,
    SmallInteger,
    Date,
    Text,
    Integer,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.base import ExchangeBase


class Contact(ExchangeBase):
    __tablename__ = "contacts"

    id = Column(String(12), primary_key=True)

    company_id = Column(String(12))

    first_name = Column(String(100))
    last_name = Column(String(100))

    job_title = Column(String(250))
    job_level = Column(String(100))

    parent_department = Column(ARRAY(String))
    department = Column(String(100))

    function = Column(String(100))

    email = Column(String(150))
    email_pattern = Column(String(50))

    work_phone = Column(String(30))
    extnumber = Column(String(10))

    personal_email = Column(String(150))

    alternate_number = Column(String(30))
    alt_ext = Column(String(10))

    alternate_number1 = Column(String(30))
    alt_ext1 = Column(String(10))

    address1 = Column(String(250))
    address2 = Column(String(250))

    city = Column(String(100))
    state = Column(String(100))

    zip_code = Column(String(10))
    country = Column(String(150))

    li_url = Column(String(250))
    twitter_url = Column(String(250))

    ivr = Column(String(100))

    source = Column(String(50))
    source_id = Column(String(50))

    comments = Column(Text)

    data_status = Column(String(50))

    linkedin_verified = Column(String(10))
    linkedin_verified_on = Column(Date)

    email_verified = Column(String(10))
    email_status = Column(String(30))
    email_verified_on = Column(Date)

    phone_verified = Column(String(10))
    phone_status = Column(String(50))
    phone_verified_on = Column(Date)

    status = Column(String(20))

    deleted = Column(Integer, default=0)

    created_by = Column(String(50))
    modified_by = Column(String(50))

    created_on = Column(
        DateTime,
        server_default=func.now(),
    )

    modified_on = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )