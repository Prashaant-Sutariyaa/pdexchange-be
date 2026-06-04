from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    LargeBinary,
    ForeignKey,
)
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.mixins import SoftDeleteMixin


class Client(SoftDeleteMixin, Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_code = Column(String, unique=True, index=True)
    # 🔹 CLIENT DETAILS
    name = Column(String, nullable=False)
    address = Column(String)
    country = Column(String)
    assigned_to = Column(Integer, ForeignKey("users.id"))

    # 🔹 FILE
    contract_file = Column(LargeBinary)
    contract_file_name = Column(String)

    # 🔹 CONTACT INFO
    first_name = Column(String)
    last_name = Column(String)
    contact_designation = Column(String)
    contact_email = Column(String)
    contact_office_number = Column(String)
    contact_mobile_number = Column(String)

    # 🔹 BILLING INFO
    billing_name = Column(String)
    billing_address = Column(String)
    billing_email = Column(String)
    billing_terms = Column(String)

    # 🔹 FLAGS
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    # 🔹 METADATA
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(Integer)
