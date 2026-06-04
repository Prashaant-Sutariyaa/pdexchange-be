from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission
from app.services.sentinel.jobs.sentinel_upload_service import create_sentinel_upload_job
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission
from app.services.sentinel.jobs.sentinel_upload_service import create_sentinel_upload_job

router = APIRouter(prefix="/sentinel/jobs", tags=["Sentinel Upload"])
router = APIRouter(prefix="/sentinel/jobs", tags=["Sentinel Upload"])


# ============================================================
# 🔹 UPLOAD JOB
# ============================================================


@router.post("/upload", dependencies=[Depends(check_permission("sentinel", "view"))])
async def upload_sentinel_job(
    department: str = Form(...),
    campaign_code: str = Form(None),
    segment_code: str = Form(None),
    priority: str = Form("Normal"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return await create_sentinel_upload_job(
        db=db,
        department=department,
        campaign_code=campaign_code,
        segment_code=segment_code,
        priority=priority,
        upload_file=file,
        user=user,
    )
