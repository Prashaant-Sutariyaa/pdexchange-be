import base64
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.campaign_segment import CampaignSegment
from app.models.campaign import Campaign
from app.models.client import Client
from app.models.campaign_segment import CampaignSegment


def validate_campaign_internal(data, existing_campaign=None):
    """
    🔹 Campaign-level validation (UPDATED RULES)

    Rules:
    - Accepted ≤ Allocation  ✅ (ONLY strict rule)

    Notes:
    - Delivered → independent
    - Rejected → independent
    - No relation between delivered, rejected, accepted
    """

    allocation = (
        data.total_allocation
        if hasattr(data, "total_allocation") and data.total_allocation is not None
        else (existing_campaign.total_allocation if existing_campaign else 0)
    )

    accepted = (
        data.total_accepted
        if hasattr(data, "total_accepted") and data.total_accepted is not None
        else (existing_campaign.total_accepted if existing_campaign else 0)
    )

    # 🔴 ONLY VALIDATION
    if accepted > allocation:
        raise HTTPException(
            400, "Accepted leads cannot be more than the total allocation."
        )


def format_campaign(
    c: Campaign,
    db: Session,
):

    total_segments = (
        db.query(CampaignSegment)
        .filter(
            CampaignSegment.campaign_id == c.id,
            CampaignSegment.is_deleted == False,
        )
        .count()
    )

    return {
        "id": c.id,
        "campaign_code": c.campaign_code,
        "campaign_name": c.campaign_name,
        "campaign_type": c.campaign_type,
        "delivery_mode": c.delivery_mode,
        "delivery_method": c.delivery_method,
        "client_id": c.client_id,
        "status": c.status,
        "start_date": str(c.start_date) if c.start_date else None,
        "end_date": str(c.end_date) if c.end_date else None,
        "total_allocation": c.total_allocation,
        "total_delivered": c.total_delivered,
        "total_accepted": c.total_accepted,
        "total_rejected": c.total_rejected,
        # ========================================================
        # 🔹 TOTAL SEGMENTS
        # ========================================================
        "total_segments": total_segments,
        "currency": c.currency,
        "cpl": c.cpl,
        "priority": c.priority,
        "campaign_document_name": c.campaign_document_name,
        "comment": c.comment,
        "is_deleted": c.is_deleted,
        "created_at": (
            c.created_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if c.created_at
            else None
        ),
        "created_by": c.created_by,
        "updated_at": (
            c.updated_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if c.updated_at
            else None
        ),
        "updated_by": c.updated_by,
    }


# 🔹 CREATE
def create_campaign(db: Session, data, user_id: int):

    # 🔹 DUPLICATE CHECK
    existing = (
        db.query(Campaign)
        .filter(
            Campaign.campaign_name.ilike(data.campaign_name),
            Campaign.is_deleted == False,
        )
        .first()
    )

    deleted_existing = (
        db.query(Campaign)
        .filter(
            Campaign.campaign_name.ilike(data.campaign_name),
            Campaign.is_deleted == True,
        )
        .first()
    )

    if existing:
        raise HTTPException(409, "Campaign already exists")

    if deleted_existing:
        raise HTTPException(409, "Campaign exists but is deleted")

    # 🔹 CLIENT VALIDATION
    client = (
        db.query(Client)
        .filter(Client.id == data.client_id, Client.is_deleted == False)
        .first()
    )

    if not client:
        raise HTTPException(400, "Client does not exist")

    # 🔹 DATE VALIDATION
    if data.end_date < data.start_date:
        raise HTTPException(400, "End date must be greater than or equal to start date")

    # 🔥 INTERNAL VALIDATION
    validate_campaign_internal(data)

    # 🔹 FILE
    file_data = None
    if data.campaign_document:
        file_data = base64.b64decode(data.campaign_document)

    now = datetime.now(timezone.utc)

    campaign = Campaign(
        campaign_name=data.campaign_name,
        campaign_type=data.campaign_type,
        delivery_mode=data.delivery_mode,
        delivery_method=data.delivery_method,
        client_id=data.client_id,
        status=data.status,
        start_date=data.start_date,
        end_date=data.end_date,
        total_allocation=data.total_allocation,
        total_delivered=data.total_delivered,
        total_accepted=data.total_accepted,
        total_rejected=data.total_rejected,
        currency=data.currency,
        cpl=data.cpl,
        priority=data.priority,
        campaign_document=file_data,
        campaign_document_name=data.campaign_document_name,
        comment=data.comment,
        created_at=now,
        updated_at=now,
        created_by=user_id,
        updated_by=user_id,
        is_deleted=False,
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    # 🔹 CLIENT CODE
    if not client.client_code:
        raise HTTPException(400, "Client code not found")

    date_str = campaign.created_at.strftime("%d%m%y")

    # 🔹 SAFE COUNTER (ID BASED)
    base36_counter = to_base36(campaign.id).zfill(4)

    campaign.campaign_code = f"{client.client_code}_{date_str}_{base36_counter}"

    db.commit()
    db.refresh(campaign)

    # ============================================================
    # 🔥 DEFAULT SEGMENT
    # ============================================================

    from app.models.campaign_segment import CampaignSegment
    from app.services.campaign_segment_service import to_base36 as seg_base36

    segment = CampaignSegment(
        campaign_id=campaign.id,
        title=campaign.campaign_name,
        segment_start_date=campaign.start_date,
        segment_end_date=campaign.end_date,
        allocation=campaign.total_allocation,
        delivered=0,
        accepted=0,
        rejected=0,
        status="Not Started",
        created_at=now,
        updated_at=now,
        created_by=user_id,
        updated_by=user_id,
        is_deleted=False,
    )

    db.add(segment)
    db.commit()
    db.refresh(segment)

    base36 = seg_base36(segment.id).zfill(5)
    segment.segment_code = f"{base36}"

    db.commit()
    db.refresh(segment)

    return format_campaign(campaign, db)


def get_campaigns(
    db: Session,
    page: int = None,
    limit: int = None,
    status: str = None,
    search: str = None,
    start_date: str = None,
    end_date: str = None,
):

    query = db.query(Campaign).filter(Campaign.is_deleted == False)

    # ============================================================
    # 🔹 STATUS FILTER
    # ============================================================

    if status and status != "all":

        query = query.filter(Campaign.status == status)

    # ============================================================
    # 🔹 SEARCH FILTER
    # ============================================================

    if search:

        search = search.strip()

        query = query.filter(
            (Campaign.campaign_code.ilike(f"%{search}%"))
            | (Campaign.campaign_name.ilike(f"%{search}%"))
        )
    # ============================================================
    # 🔹 DATE FILTER
    # ============================================================

    if start_date:

        query = query.filter(Campaign.start_date >= start_date)

    if end_date:

        query = query.filter(Campaign.end_date <= end_date)

    # ============================================================
    # 🔹 TOTAL
    # ============================================================

    total = query.count()

    # ============================================================
    # 🔹 DEFAULT ALL DATA
    # ============================================================

    if not page or not limit:

        page = 1

        limit = total if total > 0 else 1

    offset = (page - 1) * limit

    campaigns = query.order_by(Campaign.id.desc()).offset(offset).limit(limit).all()

    return {
        "data": [format_campaign(c, db) for c in campaigns],
        "page": page,
        "limit": limit,
        "total": total,
    }


# 🔹 GET ONE
def get_campaign(db: Session, campaign_id: int):
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.is_deleted == False)
        .first()
    )

    if not campaign:
        return None

    data = format_campaign(campaign, db)

    if campaign.campaign_document:
        data["campaign_document"] = base64.b64encode(campaign.campaign_document).decode(
            "utf-8"
        )
    else:
        data["campaign_document"] = None

    return data


# 🔹 DOWNLOAD
def get_campaign_file(db: Session, campaign_id: int):
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.is_deleted == False)
        .first()
    )

    if not campaign or not campaign.campaign_document:
        return None

    return campaign


# 🔹 UPDATE
def update_campaign(db: Session, campaign_id: int, data, user_id: int):

    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.is_deleted == False)
        .first()
    )

    if not campaign:
        return None

    # 🔹 DUPLICATE NAME
    if data.campaign_name:
        existing = (
            db.query(Campaign)
            .filter(
                Campaign.campaign_name.ilike(data.campaign_name),
                Campaign.id != campaign_id,
                Campaign.is_deleted == False,
            )
            .first()
        )

        if existing:
            raise HTTPException(409, "Campaign name already exists")

    # 🔹 CLIENT CHECK
    if data.client_id:
        client = (
            db.query(Client)
            .filter(Client.id == data.client_id, Client.is_deleted == False)
            .first()
        )

        if not client:
            raise HTTPException(400, "Client does not exist")

    # 🔹 DATE CHECK
    start_date = data.start_date or campaign.start_date
    end_date = data.end_date or campaign.end_date

    if start_date and end_date and end_date < start_date:
        raise HTTPException(400, "End date must be greater than or equal to start date")

    # 🔥 INTERNAL VALIDATION
    validate_campaign_internal(data, existing_campaign=campaign)
    # 🔴 VALIDATE MANUAL COMPLETION
    if data.status and data.status.lower() == "completed":

        allocation = (
            data.total_allocation
            if data.total_allocation is not None
            else campaign.total_allocation or 0
        )

        accepted = (
            data.total_accepted
            if data.total_accepted is not None
            else campaign.total_accepted or 0
        )

        if allocation != accepted:
            raise HTTPException(
                400,
                f"You can only mark this campaign as Completed when all allocated leads are accepted.",
            )

    # 🔹 UPDATE
    for field, value in data.dict(exclude_unset=True).items():
        if field == "campaign_document" and value:
            setattr(campaign, field, base64.b64decode(value))
        elif field != "is_deleted":
            setattr(campaign, field, value)

    campaign.updated_by = user_id
    campaign.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(campaign)

    return format_campaign(campaign, db)


# 🔹 DELETE
def delete_campaign(db: Session, campaign_id: int, user_id: int):
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.is_deleted == False)
        .first()
    )

    if not campaign:
        return None

    campaign.is_deleted = True
    campaign.updated_by = user_id
    campaign.updated_at = datetime.now(timezone.utc)

    db.commit()

    return True


# 🔹 Utils
def to_base36(num: int) -> str:
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    while num > 0:
        num, rem = divmod(num, 36)
        result = chars[rem] + result

    return result or "0"
