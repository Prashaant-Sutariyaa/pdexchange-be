from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.services.sentinel.activity.sentinel_activity_log_service import (
    get_activity_logs,
    get_activity_log,
)

router = APIRouter(
    prefix="/sentinel-activity-logs",
    tags=["Sentinel Activity Logs"],
)


# ============================================================
# 🔹 GET ALL
# ============================================================
@router.get(
    "/",
    dependencies=[
        Depends(check_permission("sentinel_activity_log", "view"))
    ],
)
def read_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_activity_logs(db)


# ============================================================
# 🔹 GET ONE
# ============================================================
@router.get(
    "/{log_id}",
    dependencies=[
        Depends(check_permission("sentinel_activity_log", "view"))
    ],
)
def read_one(
    log_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    log = get_activity_log(db, log_id)

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Sentinel activity log not found",
        )

    return log