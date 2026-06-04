from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)

from app.db.base import Base


class Disposition(Base):
    __tablename__ = "dispositions"

    id = Column(Integer, primary_key=True, index=True)

    disposition_code = Column(String(50), unique=True, index=True)

    call_disposition = Column(String(150))

    status = Column(String(150))

    sentinel_status = Column(String(50))

    churnable = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True))

    created_by = Column(Integer)

    updated_at = Column(DateTime(timezone=True))

    updated_by = Column(Integer)

    is_deleted = Column(Boolean, default=False)