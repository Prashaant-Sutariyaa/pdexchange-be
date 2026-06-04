from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from datetime import datetime

from app.db.base import Base
from app.db.mixins import SoftDeleteMixin


class ModulePermission(SoftDeleteMixin, Base):
    __tablename__ = "module_permissions"

    id = Column(Integer, primary_key=True, index=True)

    module_name = Column(String, nullable=False)
    menu_name = Column(String, nullable=True)
    permission_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("module_name", "permission_name", name="uq_module_permission"),
    )
