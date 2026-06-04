from pydantic import BaseModel
from typing import Optional


class CurrencyRateCreate(BaseModel):
    currency: str
    rate: float


class CurrencyRateUpdate(BaseModel):
    currency: Optional[str] = None
    rate: Optional[float] = None