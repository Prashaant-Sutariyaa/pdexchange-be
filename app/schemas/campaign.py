from pydantic import BaseModel
from typing import Optional
from datetime import date


class CampaignCreate(BaseModel):
    campaign_name: str
    campaign_type: Optional[str]
    delivery_mode: Optional[str]
    delivery_method: Optional[str]

    client_id: int

    status: Optional[str]

    start_date: date
    end_date: date

    total_allocation: Optional[int]
    total_delivered: Optional[int]
    total_accepted: Optional[int]
    total_rejected: Optional[int]

    currency: Optional[str]
    cpl: Optional[float]

    priority: Optional[str]

    campaign_document_name: Optional[str]
    campaign_document: Optional[str]

    comment: Optional[str]


class CampaignUpdate(BaseModel):
    campaign_name: Optional[str] = None
    campaign_type: Optional[str] = None
    delivery_mode: Optional[str] = None
    delivery_method: Optional[str] = None

    client_id: Optional[int] = None

    status: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    total_allocation: Optional[int] = None
    total_delivered: Optional[int] = None
    total_accepted: Optional[int] = None
    total_rejected: Optional[int] = None

    currency: Optional[str] = None
    cpl: Optional[float] = None

    priority: Optional[str] = None

    campaign_document_name: Optional[str] = None
    campaign_document: Optional[str] = None

    comment: Optional[str] = None
