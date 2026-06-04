from datetime import datetime

from sqlalchemy.orm import Session

from app.models.campaign_segment_batch_transaction import (
    CampaignSegmentBatchTransaction,
)


# ============================================================
# 🔹 PROCESS VV ROW
# ============================================================

def process_vv_row(
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
    # 🔹 UPDATE VV
    # ============================================================

    transaction.vv_number = row.get(
        "vv_number"
    )

    transaction.vv_disposition = row.get(
        "vv_disposition"
    )

    transaction.vv_agent = row.get(
        "vv_agent"
    )

    transaction.vv_timestamp = (
        datetime.utcnow()
    )

    transaction.updated_at = (
        datetime.utcnow()
    )

    transaction.updated_by = user_id

    db.commit()