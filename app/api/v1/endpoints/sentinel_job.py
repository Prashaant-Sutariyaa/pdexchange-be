from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
)

from app.core.permissions import (
    check_permission,
)
import os
from fastapi.responses import FileResponse
from sqlalchemy import or_

from app.models.sentinel_job import SentinelJob

router = APIRouter(
    prefix="/sentinel-jobs",
    tags=["Sentinel Jobs"],
)


# ============================================================
# 🔹 GET ALL
# ============================================================
@router.get("/", dependencies=[Depends(check_permission("sentinel", "view"))])
def read_all(
    page: int = 1,
    limit: int = 20,
    search: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    if page < 1:
        page = 1

    if limit < 1:
        limit = 10

    offset = (page - 1) * limit

    query = db.query(SentinelJob)

    if search:

        query = query.filter(
            or_(
                SentinelJob.campaign_codes.ilike(f"%{search}%"),
                SentinelJob.segment_codes.ilike(f"%{search}%"),
                SentinelJob.batch_codes.ilike(f"%{search}%"),
            )
        )

    query = query.order_by(SentinelJob.id.desc())

    total = query.count()

    jobs = query.offset(offset).limit(limit).all()

    return {
        "data": jobs,
        "page": page,
        "limit": limit,
        "total": total,
    }


# ============================================================
# 🔹 GET ONE
# ============================================================
@router.get(
    "/{job_id}",
    dependencies=[Depends(check_permission("sentinel", "view"))],
)
def read_one(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    job = db.query(SentinelJob).filter(SentinelJob.id == job_id).first()

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Sentinel job not found",
        )

    return job


# ============================================================
# 🔹 DOWNLOAD UPLOADED FILE
# ============================================================


@router.get(
    "/{job_id}/download-uploaded-file",
    dependencies=[Depends(check_permission("sentinel", "view"))],
)
def download_uploaded_file(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    job = db.query(SentinelJob).filter(SentinelJob.id == job_id).first()

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Sentinel job not found",
        )

    if not job.file_path:

        raise HTTPException(
            status_code=404,
            detail="Uploaded file not found",
        )

    if not os.path.exists(job.file_path):

        raise HTTPException(
            status_code=404,
            detail="File does not exist on server",
        )

    return FileResponse(
        path=job.file_path,
        filename=job.file_name,
        media_type="text/csv",
    )


# ============================================================
# 🔹 DOWNLOAD FAILED FILE
# ============================================================


@router.get(
    "/{job_id}/download-failed-file",
    dependencies=[Depends(check_permission("sentinel", "view"))],
)
def download_failed_file(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    job = db.query(SentinelJob).filter(SentinelJob.id == job_id).first()

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Sentinel job not found",
        )

    if not job.invalid_file_path:

        raise HTTPException(
            status_code=404,
            detail="Failed upload file not found",
        )

    if not os.path.exists(job.invalid_file_path):

        raise HTTPException(
            status_code=404,
            detail="File does not exist on server",
        )

    return FileResponse(
        path=job.invalid_file_path,
        filename=job.invalid_file_name,
        media_type="text/csv",
    )
