from enum import Enum

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class DerivedFrom(str, Enum):
    CRON = "cron"
    MANUAL = "manual"


class SentinelAgentProductivityResponse(BaseModel):
    id: int

    agent_id: Optional[int]

    agent_email: Optional[str]

    department: Optional[str]

    campaign_code: Optional[str]
    segment_code: Optional[str]
    batch_code: Optional[str]

    total_rows: Optional[int]
    valid_rows: Optional[int]
    invalid_rows: Optional[int]

    work_date: Optional[date]

    derived_from: Optional[DerivedFrom]

    created_at: Optional[datetime]

    class Config:
        from_attributes = True
