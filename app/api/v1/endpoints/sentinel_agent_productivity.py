from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.services.sentinel.productivity.sentinel_agent_productivity_service import (
    get_agent_productivity_list,
    get_agent_productivity,
)

router = APIRouter(
    prefix="/sentinel-agent-productivity",
    tags=["Sentinel Agent Productivity"],
)


# ============================================================
# 🔹 GET ALL
# ============================================================
@router.get(
    "/",
    dependencies=[
        Depends(check_permission("sentinel_agent_productivity", "view"))
    ],
)
def read_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_agent_productivity_list(db)


# ============================================================
# 🔹 GET ONE
# ============================================================
@router.get(
    "/{productivity_id}",
    dependencies=[
        Depends(check_permission("sentinel_agent_productivity", "view"))
    ],
)
def read_one(
    productivity_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    productivity = get_agent_productivity(db, productivity_id)

    if not productivity:
        raise HTTPException(
            status_code=404,
            detail="Sentinel agent productivity record not found",
        )

    return productivity