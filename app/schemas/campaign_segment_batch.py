from enum import Enum

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BatchStatus(str, Enum):
    IN_PROCESS = "In Process"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"


class BatchPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CampaignSegmentBatchResponse(BaseModel):
    id: int

    batch_code: str
    campaign_code: str
    segment_code: str

    dataops_valid: Optional[int]
    dataops_invalid: Optional[int]
    dataops_total: Optional[int]

    email_valid: Optional[int]
    email_invalid: Optional[int]
    email_total: Optional[int]

    quality_valid: Optional[int]
    quality_invalid: Optional[int]
    quality_total: Optional[int]

    dbr_valid: Optional[int]
    dbr_invalid: Optional[int]
    dbr_total: Optional[int]

    vv_valid: Optional[int]
    vv_invalid: Optional[int]
    vv_total: Optional[int]

    mis_valid: Optional[int]
    mis_invalid: Optional[int]
    mis_total: Optional[int]

    priority: Optional[BatchPriority] = None
    status: Optional[BatchStatus] = None

    completed_at: Optional[datetime]

    created_at: Optional[datetime]
    created_by: Optional[int]

    updated_at: Optional[datetime]
    updated_by: Optional[int]

    class Config:
        from_attributes = True
