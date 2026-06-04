from sqlalchemy.orm import Session

from app.models.campaign_segment_batch_transaction import (
    CampaignSegmentBatchTransaction,
)


# ============================================================
# 🔹 FORMAT
# ============================================================
def format_transaction(t: CampaignSegmentBatchTransaction):
    return {
        "id": t.id,
        "batch_code": t.batch_code,

        "email": t.email,
        "email_hash": t.email_hash,

        "vendor_code": t.vendor_code,

        "salutation": t.salutation,

        "first_name": t.first_name,
        "last_name": t.last_name,

        "tal_company_name": t.tal_company_name,
        "li_company_name": t.li_company_name,

        "domain": t.domain,

        "job_title": t.job_title,
        "job_level": t.job_level,
        "job_department": t.job_department,

        "work_phone": t.work_phone,
        "headquarter_phone": t.headquarter_phone,

        "contact_li_profile": t.contact_li_profile,

        "address1": t.address1,
        "address2": t.address2,

        "city": t.city,
        "state": t.state,
        "zip_code": t.zip_code,
        "country": t.country,

        "industry": t.industry,
        "sub_industry": t.sub_industry,

        "sic_code": t.sic_code,
        "naics_code": t.naics_code,

        "employee_count": t.employee_count,
        "employee_range": t.employee_range,

        "revenue_count": t.revenue_count,
        "revenue_range": t.revenue_range,

        "company_li_profile": t.company_li_profile,

        "source": t.source,

        "installbase_technology": t.installbase_technology,

        "email_validation_status": t.email_validation_status,

        "dataops_agent": t.dataops_agent,
        "dataops_timestamp": (
            t.dataops_timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if t.dataops_timestamp
            else None
        ),

        "email_status": t.email_status,
        "email_reason": t.email_reason,

        "asset1": t.asset1,
        "asset2": t.asset2,

        "ip_address": t.ip_address,

        "email_time_tool": t.email_time_tool,
        "email_agent": t.email_agent,
        "email_timestamp": (
            t.email_timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if t.email_timestamp
            else None
        ),

        "quality_status": t.quality_status,
        "quality_reason": t.quality_reason,
        "quality_agent": t.quality_agent,
        "quality_timestamp": (
            t.quality_timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if t.quality_timestamp
            else None
        ),

        "work_experience": t.work_experience,
        "activity": t.activity,
        "comments": t.comments,

        "dbr_status": t.dbr_status,
        "dbr_reason": t.dbr_reason,
        "dbr_agent": t.dbr_agent,
        "dbr_timestamp": (
            t.dbr_timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if t.dbr_timestamp
            else None
        ),

        "vv_number": t.vv_number,
        "vv_disposition": t.vv_disposition,
        "vv_agent": t.vv_agent,
        "vv_timestamp": (
            t.vv_timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if t.vv_timestamp
            else None
        ),

        "mis_status": t.mis_status,
        "mis_reason": t.mis_reason,
        "mis_agent": t.mis_agent,
        "mis_timestamp": (
            t.mis_timestamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if t.mis_timestamp
            else None
        ),

        "is_deleted": t.is_deleted,

        "created_at": (
            t.created_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if t.created_at
            else None
        ),

        "created_by": t.created_by,

        "updated_at": (
            t.updated_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if t.updated_at
            else None
        ),

        "updated_by": t.updated_by,
    }


# ============================================================
# 🔹 GET ALL
# ============================================================
def get_transactions(db: Session):

    transactions = (
        db.query(CampaignSegmentBatchTransaction)
        .filter(CampaignSegmentBatchTransaction.is_deleted == False)
        .order_by(CampaignSegmentBatchTransaction.id.desc())
        .all()
    )

    return [format_transaction(t) for t in transactions]


# ============================================================
# 🔹 GET ONE
# ============================================================
def get_transaction(db: Session, transaction_id: int):

    transaction = (
        db.query(CampaignSegmentBatchTransaction)
        .filter(
            CampaignSegmentBatchTransaction.id == transaction_id,
            CampaignSegmentBatchTransaction.is_deleted == False,
        )
        .first()
    )

    if not transaction:
        return None

    return format_transaction(transaction)