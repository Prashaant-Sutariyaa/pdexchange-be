from sqlalchemy.orm import Session

from app.models.campaign_segment_batch import CampaignSegmentBatch


# ============================================================
# 🔹 FORMAT
# ============================================================
def format_batch(batch: CampaignSegmentBatch):
    return {
        "id": batch.id,
        
        "batch_code": batch.batch_code,
        "campaign_code": batch.campaign_code,
        "segment_code": batch.segment_code,

        "dataops_valid": batch.dataops_valid,
        "dataops_invalid": batch.dataops_invalid,
        "dataops_total": batch.dataops_total,
        "email_valid": batch.email_valid,
        "email_invalid": batch.email_invalid,
        "email_total": batch.email_total,
        "quality_valid": batch.quality_valid,
        "quality_invalid": batch.quality_invalid,
        "quality_total": batch.quality_total,
        "dbr_valid": batch.dbr_valid,
        "dbr_invalid": batch.dbr_invalid,
        "dbr_total": batch.dbr_total,
        "vv_valid": batch.vv_valid,
        "vv_invalid": batch.vv_invalid,
        "vv_total": batch.vv_total,
        "mis_valid": batch.mis_valid,
        "mis_invalid": batch.mis_invalid,
        "mis_total": batch.mis_total,
        "priority": batch.priority,
        "status": batch.status,
        "completed_at": (
            batch.completed_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if batch.completed_at
            else None
        ),
        "created_at": (
            batch.created_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if batch.created_at
            else None
        ),
        "created_by": batch.created_by,
        "updated_at": (
            batch.updated_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if batch.updated_at
            else None
        ),
        "updated_by": batch.updated_by,
    }


# ============================================================
# 🔹 GET ALL (PAGINATION)
# ============================================================
def get_batches(
    db: Session,
    page: int = 1,
    limit: int = 20,
):

    offset = (page - 1) * limit

    query = db.query(CampaignSegmentBatch)

    total = query.count()

    batches = (
        query
        .order_by(CampaignSegmentBatch.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "data": [format_batch(batch) for batch in batches],
        "page": page,
        "limit": limit,
        "total": total,
    }


# ============================================================
# 🔹 GET ONE
# ============================================================
def get_batch(db: Session, batch_id: str):

    batch = (
        db.query(CampaignSegmentBatch)
        .filter(CampaignSegmentBatch.id == batch_id)
        .first()
    )

    if not batch:
        return None

    return format_batch(batch)
