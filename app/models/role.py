from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.db.base import Base
from app.db.mixins import SoftDeleteMixin


class Role(SoftDeleteMixin, Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, index=True, nullable=False)

    is_active = Column(Boolean, default=True)   # ✅ ADD THIS
    is_deleted = Column(Boolean, default=False) # ✅ KEEP THIS

    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)