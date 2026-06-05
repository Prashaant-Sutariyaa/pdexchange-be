from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from datetime import datetime

from app.db.base import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False
    )

    module_permission_id = Column(
        Integer,
        ForeignKey("module_permissions.id"),
        nullable=False
    )

    is_active = Column(Boolean, default=True)

    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "module_permission_id",
            name="uq_role_permission"
        ),
        Index(
            "idx_role_permission",
            "role_id"
        ),
    )