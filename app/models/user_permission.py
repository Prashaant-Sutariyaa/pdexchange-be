from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, Index
from datetime import datetime

from app.db.base import Base


class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_permission_id = Column(Integer, ForeignKey("module_permissions.id"), nullable=False)

    is_active = Column(Boolean, default=True)

    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "module_permission_id",
            name="uq_user_permission"
        ),
        Index("idx_user_permission", "user_id"),
    )