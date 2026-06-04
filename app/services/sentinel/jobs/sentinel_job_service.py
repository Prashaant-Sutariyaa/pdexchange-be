from datetime import datetime

from sqlalchemy.orm import Session

from app.models.sentinel_job import SentinelJob


# ============================================================
# 🔹 GET NEXT PENDING JOB
# ============================================================

def get_next_pending_job(
    db: Session,
):

    return (
        db.query(SentinelJob)
        .filter(
            SentinelJob.status == "Pending"
        )
        .order_by(SentinelJob.id.asc())
        .first()
    )


# ============================================================
# 🔹 MARK RUNNING
# ============================================================

def mark_job_running(
    db: Session,
    job: SentinelJob,
):

    job.status = "Running"

    job.started_at = datetime.utcnow()

    db.commit()

    db.refresh(job)


# ============================================================
# 🔹 MARK COMPLETED
# ============================================================

def mark_job_completed(
    db,
    job,

    output_file_name=None,
    output_file_path=None,

    invalid_file_name=None,
    invalid_file_path=None,
):

    job.status = "Completed"

    job.output_file_name = output_file_name
    job.output_file_path = output_file_path

    job.invalid_file_name = invalid_file_name
    job.invalid_file_path = invalid_file_path

    job.completed_at = datetime.utcnow()

    db.commit()

    db.refresh(job)


# ============================================================
# 🔹 MARK FAILED
# ============================================================

def mark_job_failed(
    db,
    job,
    error_message,
):

    job.status = "Failed"

    job.error_message = str(
        error_message
    )

    job.completed_at = datetime.utcnow()

    db.commit()

    db.refresh(job)