from sqlalchemy import Column, Integer, String, Float, DateTime, Date, UniqueConstraint
from app.db.base import Base


class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Integer, default=1)

    currency = Column(String, index=True)

    rate = Column(Float)

    # 🔥 NEW
    api_date = Column(Date)

    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("currency", name="uq_currency"),
    )