from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)   # who did action
    action = Column(String, nullable=False)     # create/update/delete
    module = Column(String, nullable=False)     # user, role, etc
    record_id = Column(Integer, nullable=False)

    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())