from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
)
from sqlalchemy import Enum
from app.db.base import Base
from sqlalchemy.sql import expression

class CampaignSegmentBatchTransaction(Base):
    __tablename__ = "campaign_segment_batch_transactions"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    batch_code = Column(String(30), index=True)

    email = Column(String(255))
    email_hash = Column(String(32))

    vendor_code = Column(String(10))

    salutation = Column(Text)

    first_name = Column(String(100))
    last_name = Column(String(100))

    tal_company_name = Column(String(255))
    li_company_name = Column(String(255))

    domain = Column(String(255))

    job_title = Column(String(255))
    job_level = Column(String(100))
    job_department = Column(String(100))

    work_phone = Column(String(50))
    headquarter_phone = Column(String(50))

    contact_li_profile = Column(String(255))

    address1 = Column(String(255))
    address2 = Column(String(255))

    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    country = Column(String(100))

    industry = Column(String(100))
    sub_industry = Column(String(100))

    sic_code = Column(String(10))
    naics_code = Column(String(15))

    employee_count = Column(String(50))
    employee_range = Column(String(50))

    revenue_count = Column(String(50))
    revenue_range = Column(String(50))

    company_li_profile = Column(String(255))

    source = Column(String(50))

    installbase_technology = Column(String(100))

    email_validation_status = Column(
        Enum(
            "Valid",
            "Invalid",
            "Catch-All",
            name="email_validation_status_enum",
        )
    )

    dataops_agent = Column(String(50))
    dataops_timestamp = Column(DateTime(timezone=True))

    email_status = Column(
        Enum(
            "Delivered",
            "Opened",
            "Clicked",
            "Unsubscribed",
            "Hard Bounce",
            "Soft Bounce",
            name="email_status_enum",
        )
    )
    email_reason = Column(String(255))

    asset1 = Column(String(255))
    asset2 = Column(String(255))

    ip_address = Column(String(45))

    email_time_tool = Column(String(50))
    email_agent = Column(String(50))
    email_timestamp = Column(DateTime(timezone=True))

    quality_status = Column(
        Enum(
            "Qualified",
            "Disqualified",
            name="quality_status_enum",
        )
    )
    quality_reason = Column(Text)
    quality_agent = Column(String(50))
    quality_timestamp = Column(DateTime(timezone=True))

    work_experience = Column(Text)
    activity = Column(Text)
    comments = Column(Text)

    dbr_status = Column(
        Enum(
            "Yes",
            "No",
            name="dbr_status_enum",
        )
    )
    dbr_reason = Column(Text)
    dbr_agent = Column(String(50))
    dbr_timestamp = Column(DateTime(timezone=True))

    vv_number = Column(String(50))
    vv_disposition = Column(String(255))
    vv_agent = Column(String(50))
    vv_timestamp = Column(DateTime(timezone=True))

    mis_status = Column(
        Enum(
            "RTD",
            "TBD",
            "Delivered",
            "Accepted",
            "Internal Rejected",
            "Client Rejected",
            "High CPC",
            name="mis_status_enum",
        )
    )
    mis_reason = Column(String(255))
    mis_agent = Column(String(50))
    mis_timestamp = Column(DateTime(timezone=True))

    is_deleted = Column(Boolean, nullable=False, server_default=expression.false())

    created_at = Column(DateTime(timezone=True))
    created_by = Column(Integer)

    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
