from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.services.campaign_segment_batch_service import (
    get_batches,
    get_batch,
)

router = APIRouter(
    prefix="/campaign-segment-batches",
    tags=["Campaign Segment Batches"],
)


# ============================================================
# 🔹 GET ALL
# ============================================================
# ============================================================
# 🔹 GET ALL
# ============================================================
@router.get(
    "/",
    dependencies=[
        Depends(check_permission("campaign", "view"))
    ],
)
def read_all(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_batches(db, page, limit)


# ============================================================
# 🔹 GET ONE
# ============================================================
@router.get(
    "/{batch_id}",
    dependencies=[
        Depends(check_permission("campaign", "view"))
    ],
)
def read_one(
    batch_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    batch = get_batch(db, batch_id)

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Campaign segment batch not found",
        )

    return batch