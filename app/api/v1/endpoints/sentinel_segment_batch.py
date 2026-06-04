from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission
from app.services.sentinel_segment_service import (
    get_sentinel_batch,
    get_sentinel_batches_by_segment_code,
    get_sentinel_segment_batches,
)

router = APIRouter(prefix="/sentinel-batches", tags=["Sentinel Batches"])


# ============================================================
# 🔹 GET ALL
# ============================================================
@router.get("/", dependencies=[Depends(check_permission("sentinel", "view"))])
def read_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    campaign_search: str = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_sentinel_segment_batches(
        db,
        page,
        limit,
        search,
        campaign_search,
    )


# ============================================================
# 🔹 GET BY SEGMENT CODE
# ============================================================
@router.get(
    "/segment/{segment_code}",
    dependencies=[Depends(check_permission("sentinel", "view"))],
)
def read_by_segment_code(
    segment_code: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_sentinel_batches_by_segment_code(
        db,
        segment_code,
        page,
        limit,
    )


# ============================================================
# 🔹 GET ONE
# ============================================================
@router.get(
    "/{batch_code}", dependencies=[Depends(check_permission("sentinel", "view"))]
)
def read_one(
    batch_code: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    batch = get_sentinel_batch(
        db,
        batch_code,
    )

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Sentinel batch not found",
        )

    return batch
