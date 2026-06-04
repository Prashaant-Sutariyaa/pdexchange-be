from datetime import datetime

from fastapi import HTTPException, UploadFile
import asyncio

from sqlalchemy.orm import Session

from app.models.sentinel_job import SentinelJob
from app.models.sentinel_activity_log import SentinelActivityLog

from app.services.sentinel.jobs.sentinel_processor_service import (
    process_job,
)

from app.utils.file_helper import (
    validate_csv_file,
    generate_file_hash,
    generate_sentinel_file_name,
    save_upload_file,
)


# ============================================================
# 🔹 CREATE JOB
# ============================================================

async def create_sentinel_upload_job(
    db: Session,
    department: str,
    campaign_code: str,
    segment_code: str,
    priority: str,
    upload_file: UploadFile,
    user,
):

    # ============================================================
    # 🔹 VALIDATE FILE
    # ============================================================

    if not validate_csv_file(upload_file.filename):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed",
        )

    # ============================================================
    # 🔹 DEPARTMENT RULES
    # ============================================================

    if department.lower() != "dataops":

        campaign_code = None
        segment_code = None

    # ============================================================
    # 🔹 READ FILE
    # ============================================================

    file_bytes = upload_file.file.read()

    if not file_bytes:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty",
        )

    # ============================================================
    # 🔹 HASH
    # ============================================================

    file_hash = generate_file_hash(file_bytes)

    # ============================================================
    # 🔹 FILE NAME
    # ============================================================

    stored_file_name = generate_sentinel_file_name(
        department=department,
        original_file_name=upload_file.filename,
    )

    # ============================================================
    # 🔹 SAVE FILE
    # ============================================================

    file_path = save_upload_file(
        file_bytes=file_bytes,
        file_name=stored_file_name,
    )

    # ============================================================
    # 🔹 CREATE JOB
    # ============================================================

    job = SentinelJob(
        job_type="Batch_Upload",

        department=department,

        campaign_codes=campaign_code,
        segment_codes=segment_code,

        file_name=stored_file_name,
        file_path=file_path,
        file_hash=file_hash,

        status="Pending",

        priority=priority,

        attempts=1,
        max_attempts=3,

        output_file_name=None,
        output_file_path=None,

        invalid_file_name=None,
        invalid_file_path=None,

        error_message=None,

        created_at=datetime.utcnow(),

        created_by=user.id,
    )

    db.add(job)

    db.flush()

    # ============================================================
    # 🔹 ACTIVITY LOG
    # ============================================================

    activity = SentinelActivityLog(
        user_id=user.id,

        user_role=str(user.role_id),

        job_id=job.id,

        department=department,

        batch_status="In Process",

        activity_type="Upload",

        campaign_codes=campaign_code,
        segment_codes=segment_code,

        total_rows=0,
        valid_rows=0,
        invalid_rows=0,

        file_name=stored_file_name,
        file_path=file_path,
        file_link=file_path,

        action_source="UI",

        remarks="Sentinel upload job created",

        created_at=datetime.utcnow(),
    )

    db.add(activity)

    db.commit()

    # ============================================================
    # 🔹 START ASYNC PROCESSING
    # ============================================================

    asyncio.create_task(
        process_job(job.id)
    )

    # ============================================================
    # 🔹 RESPONSE
    # ============================================================

    return {
        "message": "Sentinel upload job created successfully",

        "job_id": job.id,

        "status": job.status,
    }