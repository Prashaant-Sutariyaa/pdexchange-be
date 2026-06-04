from datetime import datetime

from sqlalchemy.orm import Session

from app.models.campaign_segment_batch import (
    CampaignSegmentBatch,
)


# ============================================================
# 🔹 GET OR CREATE BATCH
# ============================================================

def get_or_create_batch(
    db: Session,
    batch_code: str,
    campaign_code: str,
    segment_code: str,
    user_id: int,
):

    batch = (
        db.query(CampaignSegmentBatch)
        .filter(
            CampaignSegmentBatch.batch_code == batch_code
        )
        .first()
    )

    # ============================================================
    # 🔹 EXISTING BATCH
    # ============================================================

    if batch:

        batch.updated_at = datetime.utcnow()
        batch.updated_by = user_id

        db.commit()

        db.refresh(batch)

        return batch

    # ============================================================
    # 🔹 CREATE NEW BATCH
    # ============================================================

    batch = CampaignSegmentBatch(
        batch_code=batch_code,

        campaign_code=campaign_code,
        segment_code=segment_code,

        priority="medium",

        status="In Process",

        created_at=datetime.utcnow(),
        created_by=user_id,
    )

    db.add(batch)

    db.commit()

    db.refresh(batch)

    return batch