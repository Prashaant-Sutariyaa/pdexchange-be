from sqlalchemy.orm import Session

from app.models.sentinel_activity_log import SentinelActivityLog


# ============================================================
# 🔹 FORMAT
# ============================================================
def format_activity_log(log: SentinelActivityLog):
    return {
        "id": log.id,
        "user_id": log.user_id,
        "job_id": log.job_id,
        "user_role": log.user_role,
        "department": log.department,
        "activity_type": log.activity_type,
        "campaign_codes": log.campaign_codes,
        "segment_codes": log.segment_codes,
        "batch_codes": log.batch_codes,
        "batch_status": log.batch_status,
        "total_rows": log.total_rows,
        "valid_rows": log.valid_rows,
        "invalid_rows": log.invalid_rows,
        "file_name": log.file_name,
        "file_path": log.file_path,
        "file_link": log.file_link,
        "action_source": log.action_source,
        "remarks": log.remarks,
        "created_at": (
            log.created_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if log.created_at
            else None
        ),
    }


# ============================================================
# 🔹 GET ALL
# ============================================================
def get_activity_logs(db: Session):

    logs = (
        db.query(SentinelActivityLog)
        .order_by(SentinelActivityLog.created_at.desc())
        .all()
    )

    return [format_activity_log(log) for log in logs]


# ============================================================
# 🔹 GET ONE
# ============================================================
def get_activity_log(db: Session, log_id: int):

    log = db.query(SentinelActivityLog).filter(SentinelActivityLog.id == log_id).first()

    if not log:
        return None

    return format_activity_log(log)
