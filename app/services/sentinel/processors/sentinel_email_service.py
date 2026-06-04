from datetime import datetime

from sqlalchemy.orm import Session

from app.models.campaign_segment_batch_transaction import (
    CampaignSegmentBatchTransaction,
)


# ============================================================
# 🔹 PROCESS EMAIL ROW
# ============================================================

def process_email_row(
    db: Session,
    row: dict,
    user_id: int,
):

    batch_code = (
        row.get("batch_code")
        or ""
    ).strip()

    email = (
        row.get("email")
        or ""
    ).strip().lower()

    transaction = (
        db.query(
            CampaignSegmentBatchTransaction
        )
        .filter(
            CampaignSegmentBatchTransaction.batch_code
            == batch_code,

            CampaignSegmentBatchTransaction.email
            == email,
        )
        .first()
    )

    if not transaction:

        raise Exception(
            f"Transaction not found for "
            f"{batch_code} / {email}"
        )

    # ============================================================
    # 🔹 UPDATE EMAIL DATA
    # ============================================================

    transaction.email_status = row.get(
        "email_status"
    )

    transaction.email_reason = row.get(
        "email_reason"
    )

    transaction.asset1 = row.get(
        "asset1"
    )

    transaction.asset2 = row.get(
        "asset2"
    )

    transaction.ip_address = row.get(
        "ip_address"
    )

    transaction.email_time_tool = row.get(
        "email_time_tool"
    )

    transaction.email_agent = row.get(
        "email_agent"
    )

    transaction.email_timestamp = (
        datetime.utcnow()
    )

    transaction.updated_at = (
        datetime.utcnow()
    )

    transaction.updated_by = user_id

    db.commit()