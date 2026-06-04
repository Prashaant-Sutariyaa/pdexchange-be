from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


# ============================================================
# 🔹 ENUMS
# ============================================================

class SentinelJobType(str, Enum):
    BATCH_UPLOAD = "Batch_Upload"


class SentinelJobStatus(str, Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"


class SentinelJobPriority(str, Enum):
    HIGH = "High"
    NORMAL = "Normal"


# ============================================================
# 🔹 RESPONSE
# ============================================================

class SentinelJobResponse(BaseModel):
    id: int

    job_type: Optional[SentinelJobType]

    department: Optional[str]

    campaign_codes: Optional[str]
    segment_codes: Optional[str]
    batch_codes: Optional[str]

    file_name: Optional[str]
    file_path: Optional[str]
    file_hash: Optional[str]

    status: Optional[SentinelJobStatus]
    priority: Optional[SentinelJobPriority]

    attempts: Optional[int]
    max_attempts: Optional[int]

    output_file_name: Optional[str]
    output_file_path: Optional[str]

    invalid_file_name: Optional[str]
    invalid_file_path: Optional[str]

    error_message: Optional[str]

    completed_at: Optional[datetime]
    started_at: Optional[datetime]

    created_at: Optional[datetime]

    created_by: Optional[int]

    class Config:
        from_attributes = True