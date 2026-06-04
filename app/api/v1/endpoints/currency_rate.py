from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user

from app.services.currency_rate_service import (
    get_currency_rates,
)

router = APIRouter(
    prefix="/currency-rates",
    tags=["Currency Rates"]
)


# ============================================================
# 🔹 GET ALL
# ============================================================
@router.get(
    "/",
    dependencies=[Depends(get_current_user)]
)
def read_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_currency_rates(db)