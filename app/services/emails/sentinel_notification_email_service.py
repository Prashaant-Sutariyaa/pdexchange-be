from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.user import User

from app.models.sentinel_job import (
    SentinelJob,
)

from app.services.emails.email_service import (
    load_html_template,
    render_template,
    mailer,
)
from app.constants.email_recipients import (
    SENTINEL_EMAIL_RECIPIENTS,
)

# ============================================================
# 🔹 SEND SENTINEL JOB COMPLETED EMAIL
# ============================================================


async def send_sentinel_job_completed_email(
    db: Session,
    job_id: int,
):

    try:

        # ====================================================
        # 🔹 JOB
        # ====================================================

        job = db.query(SentinelJob).filter(SentinelJob.id == job_id).first()

        if not job:
            return

        # ====================================================
        # 🔹 USER
        # ====================================================

        user = db.query(User).filter(User.id == job.created_by).first()

        # ====================================================
        # 🔹 BATCH CODES
        # ====================================================

        batch_codes = []

        if job.batch_codes:

            batch_codes = [
                batch.strip() for batch in job.batch_codes.split(",") if batch.strip()
            ]

        if not batch_codes:
            return

        # ====================================================
        # 🔹 FETCH DASHBOARD SUMMARIES
        # ====================================================

        dashboard_rows = (
            db.execute(
                text("""

                SELECT *
                FROM vw_batch_dashboard_summary
                WHERE batch_code = ANY(:batch_codes)

            """),
                {"batch_codes": batch_codes},
            )
            .mappings()
            .all()
        )

        if not dashboard_rows:
            return

        # ====================================================
        # 🔹 SUMMARY TOTALS
        # ====================================================

        overall_total = 0
        overall_valid = 0
        overall_invalid = 0

        # ====================================================
        # 🔹 BATCH SUMMARIES
        # ====================================================

        batch_summaries = []

        for row in dashboard_rows:

            department_key = job.department.strip().lower()

            if department_key == "voice verification":
                department_key = "vv"

            # ================================================
            # 🔹 JOB TOTALS
            # ================================================

            job_total = row.get(
                f"{department_key}_total",
                0,
            )

            job_valid = row.get(
                f"{department_key}_valid",
                0,
            )

            job_invalid = row.get(
                f"{department_key}_invalid",
                0,
            )

            overall_total += job_total or 0

            overall_valid += job_valid or 0

            overall_invalid += job_invalid or 0

            # ================================================
            # 🔹 BATCH SUMMARY
            # ================================================

            batch_summaries.append(
                {
                    "batch_code": (row.get("batch_code") or "-"),
                    "campaign_code": (row.get("campaign_code") or "-"),
                    "segment_code": (row.get("segment_code") or "-"),
                    # ============================================
                    # DATAOPS
                    # ============================================
                    "dataops_total": (row.get("dataops_total") or 0),
                    "dataops_pending": (row.get("dataops_pending") or 0),
                    "dataops_valid": (row.get("dataops_valid") or 0),
                    "dataops_invalid": (row.get("dataops_invalid") or 0),
                    # ============================================
                    # EMAIL
                    # ============================================
                    "email_total": (row.get("email_total") or 0),
                    "email_pending": (row.get("email_pending") or 0),
                    "email_valid": (row.get("email_valid") or 0),
                    "email_invalid": (row.get("email_invalid") or 0),
                    # ============================================
                    # QUALITY
                    # ============================================
                    "quality_total": (row.get("quality_total") or 0),
                    "quality_pending": (row.get("quality_pending") or 0),
                    "quality_valid": (row.get("quality_valid") or 0),
                    "quality_invalid": (row.get("quality_invalid") or 0),
                    # ============================================
                    # DBR
                    # ============================================
                    "dbr_total": (row.get("dbr_total") or 0),
                    "dbr_pending": (row.get("dbr_pending") or 0),
                    "dbr_valid": (row.get("dbr_valid") or 0),
                    "dbr_invalid": (row.get("dbr_invalid") or 0),
                    # ============================================
                    # VV
                    # ============================================
                    "vv_total": (row.get("vv_total") or 0),
                    "vv_pending": (row.get("vv_pending") or 0),
                    "vv_valid": (row.get("vv_valid") or 0),
                    "vv_invalid": (row.get("vv_invalid") or 0),
                    # ============================================
                    # MIS
                    # ============================================
                    "mis_total": (row.get("mis_total") or 0),
                    "mis_pending": (row.get("mis_pending") or 0),
                    "mis_valid": (row.get("mis_valid") or 0),
                    "mis_invalid": (row.get("mis_invalid") or 0),
                    "mis_delivered": (row.get("mis_delivered") or 0),
                    "mis_accepted": (row.get("mis_accepted") or 0),
                    "mis_client_rejected": (row.get("mis_client_rejected") or 0),
                    "mis_rtd": (row.get("mis_rtd") or 0),
                    "mis_internal_rejected": (row.get("mis_internal_rejected") or 0),
                }
            )

        # ====================================================
        # 🔹 TEMPLATE
        # ====================================================

        html_template = load_html_template("sentinel_job_completed.html")

        # ====================================================
        # 🔹 CONTEXT
        # ====================================================

        context = {
            # ================================================
            # HEADER
            # ================================================
            "department": (job.department),
            "uploaded_by": (user.email if user else "-"),
            # ================================================
            # JOB SUMMARY
            # ================================================
            "overall_total": (overall_total),
            "overall_valid": (overall_valid),
            "overall_invalid": (overall_invalid),
            "batch_count": (len(batch_summaries)),
            # ================================================
            # BATCH SUMMARIES
            # ================================================
            "batch_summaries": (batch_summaries),
        }

        # ====================================================
        # 🔹 RENDER TEMPLATE
        # ====================================================

        html_content = render_template(
            html_template,
            context,
        )

        # ====================================================
        # 🔹 SEND EMAIL
        # ====================================================

        result = await mailer.send_mail(
            to_emails=SENTINEL_EMAIL_RECIPIENTS,
            subject=(f"Sentinel Job Completed - " f"{job.department}"),
            html_content=html_content,
        )

        print(
            "SENTINEL EMAIL RESULT:",
            result,
        )

    except Exception as e:

        print(
            "SENTINEL EMAIL ERROR:",
            str(e),
        )
