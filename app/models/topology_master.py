from sqlalchemy import (
    Column,
    Integer,
    String,
    SmallInteger,
)
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.db.base import ExchangeBase


class TopologyMaster(ExchangeBase):
    __tablename__ = "topology_master"

    id = Column(
        Integer,
        primary_key=True,
    )

    pattern = Column(
        String(15),
        nullable=False,
        unique=True,
    )

    status = Column(
        String(20),
        nullable=False,
    )

    deleted = Column(
        SmallInteger,
        default=0,
    )

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