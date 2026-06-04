from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    LargeBinary,
    ForeignKey,
    Float,
    Date,
)
from sqlalchemy.sql import func
from app.db.base import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)

    # 🔹 CODE (logic later)
    campaign_code = Column(String, unique=True, index=True)

    # 🔹 BASIC
    campaign_name = Column(String, nullable=False, index=True)
    campaign_type = Column(String)
    delivery_mode = Column(String)
    delivery_method = Column(String)

    client_id = Column(Integer, ForeignKey("clients.id"), index=True)

    status = Column(String)

    start_date = Column(Date)
    end_date = Column(Date)

    total_allocation = Column(Integer)
    total_delivered = Column(Integer)
    total_accepted = Column(Integer)
    total_rejected = Column(Integer)

    currency = Column(String)
    cpl = Column(Float)

    priority = Column(String)

    # 🔹 DOCUMENT
    campaign_document = Column(LargeBinary)
    campaign_document_name = Column(String)

    comment = Column(String)

    # 🔹 FLAGS
    is_deleted = Column(Boolean, default=False, index=True)

    # 🔹 METADATA
    created_at = Column(DateTime(timezone=True))
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True))
    updated_by = Column(Integer)
