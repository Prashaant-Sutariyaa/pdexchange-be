from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
)

from app.db.base import Base


class SentinelActivityLog(Base):
    __tablename__ = "sentinel_activity_logs"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, index=True)
    job_id = Column(Integer, index=True)

    user_role = Column(String(50))
    department = Column(String(50))

    activity_type = Column(
        Enum(
            "Upload",
            "Download",
            "Process_Complete",
            name="sentinel_activity_type_enum",
        )
    )

    campaign_codes = Column(Text)
    segment_codes = Column(Text)
    batch_codes = Column(Text)

    batch_status = Column(
        Enum(
            "In Process",
            "Paused",
            "Completed",
            "Archived",
            name="sentinel_batch_status_enum",
        )
    )

    total_rows = Column(Integer)
    valid_rows = Column(Integer)
    invalid_rows = Column(Integer)

    file_name = Column(String(255))
    file_path = Column(String(500))
    file_link = Column(String(500))

    action_source = Column(
        Enum(
            "UI",
            "CRON",
            "API",
            name="sentinel_action_source_enum",
        )
    )

    remarks = Column(Text)

    created_at = Column(DateTime(timezone=True))