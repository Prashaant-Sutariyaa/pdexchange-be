from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EmailValidationStatus(str, Enum):
    VALID = "Valid"
    INVALID = "Invalid"
    CATCH_ALL = "Catch-All"


class EmailStatus(str, Enum):
    DELIVERED = "Delivered"
    OPENED = "Opened"
    CLICKED = "Clicked"
    UNSUBSCRIBED = "Unsubscribed"
    HARD_BOUNCE = "Hard Bounce"
    SOFT_BOUNCE = "Soft Bounce"


class QualityStatus(str, Enum):
    QUALIFIED = "Qualified"
    DISQUALIFIED = "Disqualified"


class DbrStatus(str, Enum):
    YES = "Yes"
    NO = "No"


class MisStatus(str, Enum):
    RTD = "RTD"
    TBD = "TBD"
    DELIVERED = "Delivered"
    ACCEPTED = "Accepted"
    INTERNAL_REJECTED = "Internal Rejected"
    CLIENT_REJECTED = "Client Rejected"
    HIGH_CPC = "High CPC"


class CampaignSegmentBatchTransactionResponse(BaseModel):
    id: int

    batch_code: Optional[str]

    email: Optional[str]
    email_hash: Optional[str]

    vendor_code: Optional[str]

    salutation: Optional[str]

    first_name: Optional[str]
    last_name: Optional[str]

    tal_company_name: Optional[str]
    li_company_name: Optional[str]

    domain: Optional[str]

    job_title: Optional[str]
    job_level: Optional[str]
    job_department: Optional[str]

    work_phone: Optional[str]
    headquarter_phone: Optional[str]

    contact_li_profile: Optional[str]

    address1: Optional[str]
    address2: Optional[str]

    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    country: Optional[str]

    industry: Optional[str]
    sub_industry: Optional[str]

    sic_code: Optional[str]
    naics_code: Optional[str]

    employee_count: Optional[str]
    employee_range: Optional[str]

    revenue_count: Optional[str]
    revenue_range: Optional[str]

    company_li_profile: Optional[str]

    source: Optional[str]

    installbase_technology: Optional[str]

    email_validation_status: Optional[EmailValidationStatus]

    dataops_agent: Optional[str]
    dataops_timestamp: Optional[datetime]

    email_status: Optional[EmailStatus]
    email_reason: Optional[str]

    asset1: Optional[str]
    asset2: Optional[str]

    ip_address: Optional[str]

    email_time_tool: Optional[str]
    email_agent: Optional[str]
    email_timestamp: Optional[datetime]

    quality_status: Optional[QualityStatus]
    quality_reason: Optional[str]
    quality_agent: Optional[str]
    quality_timestamp: Optional[datetime]

    work_experience: Optional[str]
    activity: Optional[str]
    comments: Optional[str]

    dbr_status: Optional[DbrStatus]
    dbr_reason: Optional[str]
    dbr_agent: Optional[str]
    dbr_timestamp: Optional[datetime]

    vv_number: Optional[str]
    vv_disposition: Optional[str]
    vv_agent: Optional[str]
    vv_timestamp: Optional[datetime]

    mis_status: Optional[MisStatus]
    mis_reason: Optional[str]
    mis_agent: Optional[str]
    mis_timestamp: Optional[datetime]

    is_deleted: Optional[bool]

    created_at: Optional[datetime]
    created_by: Optional[int]

    updated_at: Optional[datetime]
    updated_by: Optional[int]

    class Config:
        from_attributes = True
