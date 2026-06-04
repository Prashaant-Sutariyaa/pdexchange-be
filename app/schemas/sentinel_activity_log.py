from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


# ============================================================
# 🔹 ENUMS
# ============================================================

class SentinelActivityType(str, Enum):
    UPLOAD = "Upload"
    DOWNLOAD = "Download"
    PROCESS_COMPLETE = "Process_Complete"


class SentinelBatchStatus(str, Enum):
    IN_PROCESS = "In Process"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"


class SentinelActionSource(str, Enum):
    UI = "UI"
    CRON = "CRON"
    API = "API"


# ============================================================
# 🔹 RESPONSE
# ============================================================

class SentinelActivityLogResponse(BaseModel):
    id: int

    user_id: Optional[int]
    job_id: Optional[int]

    user_role: Optional[str]
    department: Optional[str]

    activity_type: Optional[SentinelActivityType]

    campaign_codes: Optional[str]
    segment_codes: Optional[str]
    batch_codes: Optional[str]

    batch_status: Optional[SentinelBatchStatus]

    total_rows: Optional[int]
    valid_rows: Optional[int]
    invalid_rows: Optional[int]

    file_name: Optional[str]
    file_path: Optional[str]
    file_link: Optional[str]

    action_source: Optional[SentinelActionSource]

    remarks: Optional[str]

    created_at: Optional[datetime]

    class Config:
        from_attributes = True