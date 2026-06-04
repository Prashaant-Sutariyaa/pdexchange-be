from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.responses import StreamingResponse

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.services.revenue_service import (
    get_revenue,
    download_revenue_csv,
    get_revenue_summary,
    download_revenue_summary_csv,
    get_revenue_stats,
)

router = APIRouter(prefix="/revenue", tags=["Revenue"])


# ============================================================
# 🔹 REVENUE LIST
# ============================================================


@router.get("/", dependencies=[Depends(check_permission("revenue", "view"))])
def read_revenue(
    status: Optional[str] = None,
    client_id: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_revenue(
        db,
        status,
        client_id,
        from_date,
        to_date,
        page,
        limit,
    )


# ============================================================
# 🔹 DOWNLOAD CSV
# ============================================================


@router.get(
    "/download", dependencies=[Depends(check_permission("revenue", "download"))]
)
def download_revenue(
    status: Optional[str] = None,
    client_id: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    file = download_revenue_csv(
        db,
        status,
        client_id,
        from_date,
        to_date,
    )

    return StreamingResponse(
        file,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=revenue_report.csv"},
    )


# ============================================================
# 🔹 SUMMARY
# ============================================================


@router.get("/summary", dependencies=[Depends(check_permission("revenue", "view"))])
def revenue_summary(
    status: Optional[str] = None,
    client_id: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db: Session = Depends(get_db),
    order: str = "asc",
    user=Depends(get_current_user),
):

    return get_revenue_summary(
        db,
        status,
        client_id,
        from_date,
        to_date,
        order,
    )


# ============================================================
# 🔹 SUMMARY DOWNLOAD
# ============================================================


@router.get(
    "/summary/download", dependencies=[Depends(check_permission("revenue", "download"))]
)
def download_revenue_summary(
    status: Optional[str] = None,
    client_id: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    file = download_revenue_summary_csv(
        db,
        status,
        client_id,
        from_date,
        to_date,
    )

    return StreamingResponse(
        file,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=revenue_summary.csv"},
    )


# ============================================================
# 🔹 REVENUE STATS
# ============================================================


@router.get("/stats", dependencies=[Depends(check_permission("revenue", "view"))])
def revenue_stats(
    status: Optional[str] = None,
    client_id: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return get_revenue_stats(
        db,
        status,
        client_id,
        from_date,
        to_date,
    )
