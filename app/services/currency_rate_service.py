from datetime import datetime, timezone
from sqlalchemy.orm import Session
import requests

from app.models.currency_rate import CurrencyRate


# ============================================================
# 🔹 FORMAT
# ============================================================
def format_currency_rate(c):
    return {
        "id": c.id,
        "amount": c.amount,
        "currency": c.currency,
        "rate": c.rate,
        "api_date": str(c.api_date) if c.api_date else None,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None,
    }


# ============================================================
# 🔹 GET ALL
# ============================================================
def get_currency_rates(db: Session):
    rates = db.query(CurrencyRate).order_by(CurrencyRate.currency.asc()).all()

    return [format_currency_rate(r) for r in rates]


# ============================================================
# 🔥 AUTO SYNC CURRENCY RATES
# ============================================================
def sync_currency_rates(db: Session):

    # ========================================================
    # 🔥 CHECK LAST UPDATE TIME (12 HOURS)
    # ========================================================
    latest = db.query(CurrencyRate).order_by(CurrencyRate.updated_at.desc()).first()

    if latest and latest.updated_at:

        # 🔥 FORCE SYNC IF api_date IS NULL
        if latest.api_date is None:
            pass

        else:

            now_utc = datetime.now(timezone.utc)

            latest_updated = latest.updated_at

            if latest_updated.tzinfo is None:
                latest_updated = latest_updated.replace(tzinfo=timezone.utc)

            diff = now_utc - latest_updated

            # skip if updated within 12 hours
            if diff.total_seconds() < 43200:
                return

    # ========================================================
    # 🔥 EXTERNAL API
    # ========================================================
    response = requests.get(
        "https://api.frankfurter.dev/v1/latest?from=USD", timeout=10
    )

    if response.status_code != 200:
        return

    data = response.json()

    external_api_date = data.get("date")

    if not external_api_date:
        return

    rates = data.get("rates", {})

    # ========================================================
    # 🔥 CHECK EXISTING API DATE
    # ========================================================
    existing_record = db.query(CurrencyRate).first()

    if (
        existing_record
        and existing_record.api_date
        and str(existing_record.api_date) == external_api_date
    ):
        return

    now = datetime.now(timezone.utc)

    # ========================================================
    # 🔥 ONLY STORE REQUIRED CURRENCIES
    # ========================================================
    currencies = {
        "USD": 1,
        "GBP": rates.get("GBP"),
        "EUR": rates.get("EUR"),
        "INR": rates.get("INR"),
    }

    for currency, rate in currencies.items():

        if rate is None:
            continue

        existing = (
            db.query(CurrencyRate).filter(CurrencyRate.currency == currency).first()
        )

        if existing:

            existing.rate = rate
            existing.api_date = external_api_date
            existing.updated_at = now

        else:

            new_rate = CurrencyRate(
                amount=1,
                currency=currency,
                rate=rate,
                api_date=external_api_date,
                created_at=now,
                updated_at=now,
            )

            db.add(new_rate)

    db.commit()
