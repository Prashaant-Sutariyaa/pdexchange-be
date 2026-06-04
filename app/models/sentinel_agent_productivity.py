from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Date,
    DateTime,
)

from app.db.base import Base
from sqlalchemy import Enum

class SentinelAgentProductivity(Base):
    __tablename__ = "sentinel_agent_productivity"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    agent_id = Column(Integer, index=True)

    agent_email = Column(String(255))

    department = Column(String(50))

    campaign_code = Column(String(20))
    segment_code = Column(String(5))
    batch_code = Column(String(6))

    total_rows = Column(Integer)
    valid_rows = Column(Integer)
    invalid_rows = Column(Integer)

    work_date = Column(Date)

    derived_from = Column(
        Enum(
            "cron",
            "manual",
            name="derived_from_enum",
        )
    )

    created_at = Column(DateTime(timezone=True))