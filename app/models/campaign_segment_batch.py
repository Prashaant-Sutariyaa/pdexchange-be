from sqlalchemy import (
    CHAR,
    Column,
    Enum,
    String,
    Integer,
    SmallInteger,
    DateTime,
    ForeignKey,
)

from app.db.base import Base


class CampaignSegmentBatch(Base):
    __tablename__ = "campaign_segment_batches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    batch_code = Column(CHAR(6), unique=True, index=True)
    campaign_code = Column(CHAR(20), index=True)
    segment_code = Column(CHAR(5), index=True)

    # DATAOPS
    dataops_valid = Column(SmallInteger, default=0)
    dataops_invalid = Column(SmallInteger, default=0)
    dataops_total = Column(SmallInteger, default=0)

    # EMAIL
    email_valid = Column(SmallInteger, default=0)
    email_invalid = Column(SmallInteger, default=0)
    email_total = Column(SmallInteger, default=0)

    # QUALITY
    quality_valid = Column(SmallInteger, default=0)
    quality_invalid = Column(SmallInteger, default=0)
    quality_total = Column(SmallInteger, default=0)

    # DBR
    dbr_valid = Column(SmallInteger, default=0)
    dbr_invalid = Column(SmallInteger, default=0)
    dbr_total = Column(SmallInteger, default=0)

    # VV
    vv_valid = Column(SmallInteger, default=0)
    vv_invalid = Column(SmallInteger, default=0)
    vv_total = Column(SmallInteger, default=0)

    # MIS
    mis_valid = Column(SmallInteger, default=0)
    mis_invalid = Column(SmallInteger, default=0)
    mis_total = Column(SmallInteger, default=0)

    priority = Column(
        Enum(
            "high",
            "medium",
            "low",
            name="batch_priority_enum",
        )
    )

    status = Column(
        Enum(
            "In Process",
            "Paused",
            "Completed",
            "Archived",
            name="batch_status_enum",
        )
    )

    completed_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True))
    created_by = Column(Integer)

    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
