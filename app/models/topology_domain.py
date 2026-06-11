from sqlalchemy import (
    Column,
    String,
    Integer,
    SmallInteger,
)
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.base import ExchangeBase


class TopologyDomain(ExchangeBase):
    __tablename__ = "topology_domain"

    id = Column(Integer, primary_key=True)

    company_id = Column(String(36))
    company_location_id = Column(String(12))

    domain = Column(String(250), nullable=False)

    country = Column(String(100))

    email_domain = Column(String(250))

    pattern = Column(String(15), nullable=False)

    priority = Column(String(10))

    source = Column(String(10))

    status = Column(String(20))

    deleted = Column(SmallInteger, default=0)

    created_by = Column(Integer)
    modified_by = Column(Integer)

    created_on = Column(
        DateTime,
        server_default=func.now(),
    )

    modified_on = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )