from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    SmallInteger,
    DateTime,
    Enum,
)

from app.db.base import Base


class SentinelJob(Base):
    __tablename__ = "sentinel_jobs"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    job_type = Column(
        Enum(
            "Batch_Upload",
            name="sentinel_job_type_enum",
        )
    )

    department = Column(String(50))

    campaign_codes = Column(Text)
    segment_codes = Column(Text)
    batch_codes = Column(Text)

    file_name = Column(String(255))
    file_path = Column(String(500))
    file_hash = Column(String(64))

    status = Column(
        Enum(
            "Pending",
            "Running",
            "Completed",
            "Failed",
            name="sentinel_job_status_enum",
        )
    )

    priority = Column(
        Enum(
            "High",
            "Normal",
            name="sentinel_job_priority_enum",
        )
    )

    attempts = Column(SmallInteger, default=1)
    max_attempts = Column(SmallInteger, default=3)

    output_file_name = Column(String(255))
    output_file_path = Column(String(500))

    invalid_file_name = Column(String(255))
    invalid_file_path = Column(String(500))

    error_message = Column(Text)

    completed_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True))

    created_by = Column(Integer)