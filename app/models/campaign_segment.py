from sqlalchemy import CHAR, Column, Enum, Integer, String, Boolean, DateTime, ForeignKey, Date
from app.db.base import Base


class CampaignSegment(Base):
    __tablename__ = "campaign_segments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    segment_code = Column(CHAR(5), unique=True, index=True)

    campaign_id = Column(Integer, ForeignKey("campaigns.id"), index=True)

    title = Column(String, index=True)

    segment_start_date = Column(Date)
    segment_end_date = Column(Date)

    allocation = Column(Integer)
    delivered = Column(Integer)
    accepted = Column(Integer)
    rejected = Column(Integer)
    unrealized = Column(Integer, default=0)

    status = Column(
    Enum(
        'Not Started',
        'Cancelled',
        'Completed',
        'Live',
        'Pause',
        name='campaign_status_enum'
    )
)

    is_deleted = Column(Boolean, default=False, index=True)

    unrealized_reason = Column(String)
    created_at = Column(DateTime(timezone=True))
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
