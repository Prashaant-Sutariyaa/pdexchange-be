from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.services.campaign_segment_service import (
    bulk_upsert_segments,
    get_segments,
    get_all_segments_service,
)
from app.schemas.campaign_segment import BulkSegmentRequest
from app.core.permissions import check_permission

router = APIRouter(prefix="/campaign-segments", tags=["Campaign Segments"])


# 🔥 BULK UPSERT
@router.patch(
    "/bulk", dependencies=[Depends(check_permission("campaign_segment", "edit"))]
)
def bulk_update(
    data: BulkSegmentRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return bulk_upsert_segments(db, data, user.id)


# 🔹 GET SEGMENTS (BY CAMPAIGN)
@router.get(
    "/{campaign_id}",
    dependencies=[Depends(check_permission("campaign_segment", "view"))],
)
def read_all(
    campaign_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return get_segments(db, campaign_id)


# 🔹 GET ALL SEGMENTS
@router.get("/", dependencies=[Depends(check_permission("campaign_segment", "view"))])
def get_all_segments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_all_segments_service(db)
