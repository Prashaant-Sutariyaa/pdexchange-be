from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum


# ============================================================
# 🔹 STATUS ENUM
# ============================================================
class CampaignStatus(str, Enum):
    NOT_STARTED = "Not Started"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    LIVE = "Live"
    PAUSE = "Pause"


# ============================================================
# 🔹 SEGMENT ITEM
# ============================================================
class SegmentItem(BaseModel):
    id: Optional[int] = None

    title: str

    segment_start_date: date
    segment_end_date: date

    allocation: int
    delivered: int
    accepted: int
    rejected: int

    unrealized_reason: Optional[str] = None

    status: Optional[CampaignStatus] = None


# ============================================================
# 🔹 BULK REQUEST
# ============================================================
class BulkSegmentRequest(BaseModel):
    campaign_id: int
    segments: List[SegmentItem]