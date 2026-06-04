from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.campaign_segment import CampaignSegment
from app.models.campaign import Campaign


# ============================================================
# 🔹 BASE36
# ============================================================
def to_base36(num: int) -> str:
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while num > 0:
        num, rem = divmod(num, 36)
        result = chars[rem] + result
    return result or "0"


# ============================================================
# 🔹 FORMAT
# ============================================================
def format_segment(s: CampaignSegment):
    return {
        "id": s.id,
        "segment_code": s.segment_code,
        "campaign_id": s.campaign_id,
        "title": s.title,
        "segment_start_date": str(s.segment_start_date),
        "segment_end_date": str(s.segment_end_date),
        "allocation": s.allocation,
        "delivered": s.delivered,
        "accepted": s.accepted,
        "rejected": s.rejected,
        "unrealized": s.unrealized,
        "unrealized_reason": s.unrealized_reason,
        "status": s.status,
        "is_deleted": s.is_deleted,
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "updated_at": s.updated_at.isoformat() if s.updated_at else None,
    }


# ============================================================
# 🔥 HELPER 1: VALIDATE TOTALS
# ============================================================
def validate_segment_totals(segments, campaign):
    total_allocation = sum(s.allocation for s in segments)
    total_delivered = sum(s.delivered for s in segments)
    total_accepted = sum(s.accepted for s in segments)
    total_rejected = sum(s.rejected for s in segments)

    if total_allocation != (campaign.total_allocation or 0):
        raise HTTPException(
            400, "Please distribute full allocation across all segments."
        )

    if total_delivered != (campaign.total_delivered or 0):
        raise HTTPException(400, "Delivered values must match the campaign total.")

    if total_accepted != (campaign.total_accepted or 0):
        raise HTTPException(400, "Accepted values must match the campaign total.")

    if total_rejected != (campaign.total_rejected or 0):
        raise HTTPException(400, "Rejected values must match the campaign total.")


# ============================================================
# 🔥 HELPER 2: VALIDATE EACH SEGMENT
# ============================================================
def validate_each_segment(segments, campaign):
    for s in segments:

        if s.allocation <= 0:
            raise HTTPException(400, "Allocation must be greater than zero.")

        if s.accepted > s.allocation:
            raise HTTPException(400, "Accepted leads cannot exceed allocation.")

        # 🔥 DATE VALIDATION
        if s.segment_start_date < campaign.start_date:
            raise HTTPException(
                400,
                "Segment start date cannot be earlier than the campaign start date.",
            )

        if s.segment_end_date > campaign.end_date:
            raise HTTPException(
                400, "Segment end date cannot be later than the campaign end date."
            )

        if s.segment_end_date < s.segment_start_date:
            raise HTTPException(400, "Segment end date must be after start date.")


# ============================================================
# 🔥 HELPER 3: SOFT DELETE SYNC
# ============================================================
def sync_deleted_segments(db: Session, campaign_id, incoming_segments, user_id, now):

    existing_segments = (
        db.query(CampaignSegment)
        .filter(
            CampaignSegment.campaign_id == campaign_id,
            CampaignSegment.is_deleted == False,
        )
        .all()
    )

    existing_ids = {seg.id for seg in existing_segments}
    incoming_ids = {s.id for s in incoming_segments if s.id}

    to_delete_ids = existing_ids - incoming_ids

    deleted_ids = []

    for seg in existing_segments:
        if seg.id in to_delete_ids:
            seg.is_deleted = True
            seg.updated_by = user_id
            seg.updated_at = now
            deleted_ids.append(seg.id)

    return deleted_ids


# ============================================================
# 🔥 BULK UPSERT SEGMENTS
# ============================================================


def bulk_upsert_segments(
    db: Session,
    data,
    user_id: int,
):

    from datetime import datetime, timezone

    from app.models.campaign import Campaign
    from app.models.campaign_segment import CampaignSegment

    now = datetime.now(timezone.utc)

    # ============================================================
    # 🔹 CAMPAIGN
    # ============================================================

    campaign = (
        db.query(Campaign)
        .filter(
            Campaign.id == data.campaign_id,
            Campaign.is_deleted == False,
        )
        .first()
    )

    if not campaign:

        raise HTTPException(
            404,
            "Campaign not found",
        )

    # ============================================================
    # 🔹 TOTAL ALLOCATION VALIDATION
    # ============================================================

    total_allocation = sum(
        (segment.allocation or 0)
        for segment in data.segments
    )


    if total_allocation != (campaign.total_allocation or 0):

        raise HTTPException(
            400,
            ("Total segment allocation must match " "campaign allocation."),
        )

    # ============================================================
    # 🔹 UPSERT SEGMENTS
    # ============================================================

    for item in data.segments:

        # ========================================================
        # 🔹 UPDATE
        # ========================================================

        if item.id:

            segment = (
                db.query(CampaignSegment)
                .filter(
                    CampaignSegment.id == item.id,
                    CampaignSegment.campaign_id == campaign.id,
                    CampaignSegment.is_deleted == False,
                )
                .first()
            )

            if not segment:

                raise HTTPException(
                    404,
                    f"Segment not found: {item.id}",
                )

            # ====================================================
            # 🔹 VALIDATIONS
            # ====================================================

            allocation = item.allocation or 0
            accepted = item.accepted or 0

            if accepted > allocation:

                raise HTTPException(
                    400,
                    (
                        f"Accepted cannot be greater than "
                        f"allocation in segment "
                        f"{segment.segment_code}"
                    ),
                )

            # ====================================================
            # 🔹 UPDATE FIELDS
            # ====================================================

            for field, value in item.dict(exclude_unset=True).items():

                if field not in [
                    "id",
                    "segment_code",
                    "campaign_id",
                ]:

                    setattr(
                        segment,
                        field,
                        value,
                    )

            segment.updated_by = user_id
            segment.updated_at = now

        # ========================================================
        # 🔹 CREATE
        # ========================================================

        else:

            allocation = item.allocation or 0
            accepted = item.accepted or 0

            if accepted > allocation:

                raise HTTPException(
                    400,
                    ("Accepted cannot be greater than " "allocation."),
                )

            segment = CampaignSegment(
                campaign_id=campaign.id,
                title=item.title,
                segment_start_date=item.segment_start_date,
                segment_end_date=item.segment_end_date,
                allocation=item.allocation,
                delivered=item.delivered,
                accepted=item.accepted,
                rejected=item.rejected,
                status=item.status,
                created_at=now,
                updated_at=now,
                created_by=user_id,
                updated_by=user_id,
                is_deleted=False,
            )

            db.add(segment)

            db.flush()

            # ====================================================
            # 🔹 SEGMENT CODE
            # ====================================================

            base36 = to_base36(segment.id).zfill(5)

            segment.segment_code = f"{base36}"

    # ============================================================
    # 🔥 AGGREGATE SEGMENT TOTALS → CAMPAIGN
    # ============================================================

    active_segments = (
        db.query(CampaignSegment)
        .filter(
            CampaignSegment.campaign_id == campaign.id,
            CampaignSegment.is_deleted == False,
        )
        .all()
    )

    campaign.total_delivered = sum((s.delivered or 0) for s in active_segments)

    campaign.total_accepted = sum((s.accepted or 0) for s in active_segments)

    campaign.total_rejected = sum((s.rejected or 0) for s in active_segments)

    campaign.updated_by = user_id
    campaign.updated_at = now

    # ============================================================
    # 🔹 COMMIT
    # ============================================================

    db.commit()

    return {"message": "Segments updated successfully"}


# ============================================================
# 🔹 GET SEGMENTS
# ============================================================
def get_segments(
    db: Session,
    campaign_id: int,
):

    segments = (
        db.query(CampaignSegment)
        .join(
            Campaign,
            Campaign.id == CampaignSegment.campaign_id,
        )
        .filter(
            CampaignSegment.campaign_id == campaign_id,
            CampaignSegment.is_deleted == False,
            Campaign.is_deleted == False,
        )
        .order_by(CampaignSegment.id.desc())
        .all()
    )

    return [format_segment(s) for s in segments]


# ============================================================
# 🔹 GET ALL SEGMENTS
# ============================================================
def get_all_segments_service(
    db: Session,
):

    segments = (
        db.query(CampaignSegment)
        .join(
            Campaign,
            Campaign.id == CampaignSegment.campaign_id,
        )
        .filter(
            CampaignSegment.is_deleted == False,
            Campaign.is_deleted == False,
        )
        .order_by(CampaignSegment.id.desc())
        .all()
    )

    return [format_segment(s) for s in segments]
