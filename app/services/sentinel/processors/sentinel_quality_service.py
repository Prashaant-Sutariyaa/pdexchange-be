from datetime import datetime

from sqlalchemy.orm import Session

from app.models.campaign_segment_batch_transaction import (
    CampaignSegmentBatchTransaction,
)


# ============================================================
# 🔹 PROCESS QUALITY ROW
# ============================================================

def process_quality_row(
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
    # 🔹 UPDATE QUALITY
    # ============================================================

    transaction.quality_status = row.get(
        "quality_status"
    )

    transaction.quality_reason = row.get(
        "quality_reason"
    )

    transaction.work_experience = row.get(
        "work_experience"
    )

    transaction.activity = row.get(
        "activity"
    )

    transaction.comments = row.get(
        "comments"
    )

    transaction.quality_agent = row.get(
        "quality_agent"
    )

    transaction.quality_timestamp = (
        datetime.utcnow()
    )

    transaction.updated_at = (
        datetime.utcnow()
    )

    transaction.updated_by = user_id

    db.commit()