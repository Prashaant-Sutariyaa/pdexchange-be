import csv
import io

from sqlalchemy.orm import Session

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from app.models.campaign_segment_batch_transaction import (
    CampaignSegmentBatchTransaction,
)

from app.services.sentinel.exports.sentinel_download_permissions import (
    has_download_permission,
)

# ============================================================
# 🔹 COMMON LEAD COLUMNS
# ============================================================

COMMON_LEAD_COLUMNS = [

    ("Salutations", "salutation"),

    ("First Name", "first_name"),
    ("Last Name", "last_name"),

    ("Work Email", "email"),

    ("TAL Company Name", "tal_company_name"),

    ("Linkedin Company Name", "li_company_name"),

    ("Domain", "domain"),

    ("Job Title", "job_title"),
    ("Job Level", "job_level"),
    ("Job Department", "job_department"),

    ("WorkPhone", "work_phone"),

    ("Headquarter Phone", "headquarter_phone"),

    ("Contact Linkedin Profile", "contact_li_profile"),

    ("Address 1", "address1"),
    ("Address 2", "address2"),

    ("City", "city"),
    ("State", "state"),
    ("Zip Code", "zip_code"),
    ("Country", "country"),

    ("Industry", "industry"),
    ("Sub Industry", "sub_industry"),

    ("SIC Code", "sic_code"),
    ("NAICS Code", "naics_code"),

    ("Employees Count", "employee_count"),
    ("Employees Range", "employee_range"),

    ("Revenue Count", "revenue_count"),
    ("Revenue Range ($)", "revenue_range"),

    ("Company Linkedin Profile", "company_li_profile"),

    ("Source", "source"),

    ("Install Base Technology", "installbase_technology"),
]

# ============================================================
# 🔹 EXPORT MAPPINGS
# ============================================================

EXPORT_MAPPINGS = {

    # ========================================================
    # DATAOPS
    # ========================================================

    "dataops": [

        ("Batch ID", "batch_code"),

        ("DataOps Agent", "dataops_agent"),

        ("Vendor Code", "vendor_code"),

        *COMMON_LEAD_COLUMNS,

        ("Email Validation Status", "email_validation_status"),
    ],

    # ========================================================
    # EMAIL
    # ========================================================

    "email": [

        ("Batch ID", "batch_code"),

        ("Email Agent", "email_agent"),

        ("Work Email", "email"),

        ("Email Status", "email_status"),

        ("Email Reason", "email_reason"),

        ("Asset1", "asset1"),
        ("Asset2", "asset2"),

        ("IP Address", "ip_address"),

        ("Email_TimeStamp", "email_timestamp"),
    ],

    # ========================================================
    # QUALITY
    # ========================================================

    "quality": [

        ("Batch ID", "batch_code"),

        ("Quality Agent", "quality_agent"),

        ("Quality Status", "quality_status"),

        ("Quality Reason", "quality_reason"),

        ("Work Experience", "work_experience"),

        ("Activity", "activity"),

        ("Comments", "comments"),

        *COMMON_LEAD_COLUMNS,
    ],

    # ========================================================
    # DBR
    # ========================================================

    "dbr": [

        ("Batch ID", "batch_code"),

        ("DBR Agent", "dbr_agent"),

        ("DBR Status", "dbr_status"),

        *COMMON_LEAD_COLUMNS,
    ],

    # ========================================================
    # VV
    # ========================================================

    "vv": [

        ("Batch ID", "batch_code"),

        ("VV Agent", "vv_agent"),

        ("Work Email", "email"),

        ("VV Number", "vv_number"),

        ("VV Disposition", "vv_disposition"),
    ],

    # ========================================================
    # MIS
    # ========================================================

    "mis": [

        ("Batch ID", "batch_code"),

        ("MIS Agent", "mis_agent"),

        ("Work Email", "email"),

        ("MIS Status", "mis_status"),

        ("MIS Reason", "mis_reason"),
    ],
}


# ============================================================
# 🔹 BUILD METRIC FILTER
# ============================================================

def build_metric_filter(
    department: str,
    metric: str,
):

    t = CampaignSegmentBatchTransaction

    filters = {

        # ========================================================
        # DATAOPS
        # ========================================================

        ("dataops", "total"): (
            t.email_validation_status.is_not(None)
        ),

        ("dataops", "valid"): (
            t.email_validation_status.in_(
                ["Valid", "Catch-All"]
            )
        ),

        ("dataops", "invalid"): (
            t.email_validation_status == "Invalid"
        ),

        # ========================================================
        # EMAIL
        # ========================================================

        ("email", "total"): (
            t.email_validation_status.in_(
                ["Valid", "Catch-All"]
            )
        ),

        ("email", "pending"): (
            t.email_validation_status.in_(
                ["Valid", "Catch-All"]
            )
            &
            (t.email_status.is_(None))
        ),

        ("email", "valid"): (
            t.email_status.in_(
                ["Delivered", "Opened", "Clicked"]
            )
        ),

        ("email", "invalid"): (
            t.email_status.in_(
                ["Hard Bounce", "Soft Bounce"]
            )
        ),

        # ========================================================
        # QUALITY
        # ========================================================

        ("quality", "total"): (
            t.email_status.in_(
                ["Delivered", "Opened", "Clicked"]
            )
        ),

        ("quality", "pending"): (
            t.email_status.in_(
                ["Delivered", "Opened", "Clicked"]
            )
            &
            (t.quality_status.is_(None))
        ),

        ("quality", "valid"): (
            t.quality_status == "Qualified"
        ),

        ("quality", "invalid"): (
            t.quality_status == "Disqualified"
        ),

        # ========================================================
        # DBR
        # ========================================================

        ("dbr", "total"): (
            t.quality_status == "Qualified"
        ),

        ("dbr", "pending"): (
            (t.quality_status == "Qualified")
            &
            (t.dbr_status.is_(None))
        ),

        ("dbr", "valid"): (
            t.dbr_status == "Yes"
        ),

        ("dbr", "invalid"): (
            t.dbr_status == "No"
        ),

        # ========================================================
        # VV
        # ========================================================

        ("vv", "total"): (
            t.dbr_status == "Yes"
        ),

        ("vv", "pending"): (
            (t.dbr_status == "Yes")
            &
            (t.vv_disposition.is_(None))
        ),

        ("vv", "valid"): (
            t.vv_disposition.is_not(None)
        ),

        # ========================================================
        # MIS
        # ========================================================

        ("mis", "total"): (
            t.vv_disposition.is_not(None)
        ),

        ("mis", "pending"): (
            t.vv_disposition.is_not(None)
            &
            (t.mis_status.is_(None))
        ),

        ("mis", "delivered"): (
            t.mis_status == "Delivered"
        ),

        ("mis", "accepted"): (
            t.mis_status == "Accepted"
        ),

        ("mis", "client_rejected"): (
            t.mis_status == "Client Rejected"
        ),

        ("mis", "rtd"): (
            t.mis_status == "RTD"
        ),

        ("mis", "internal_rejected"): (
            t.mis_status == "Internal Rejected"
        ),
    }

    return filters.get(
        (department.lower(), metric.lower())
    )


# ============================================================
# 🔹 EXPORT CSV
# ============================================================

def export_metric_csv(
    db: Session,
    batch_code: str,
    department: str,
    metric: str,
    user_department: str,
):

    department = department.lower()

    metric = metric.lower()

    # ============================================================
    # 🔹 VALIDATE PERMISSION
    # ============================================================

    allowed = has_download_permission(
        user_department=user_department,
        department=department,
        metric=metric,
    )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail=(
                "You are not allowed "
                "to download this data."
            ),
        )

    # ============================================================
    # 🔹 VALIDATE DEPARTMENT
    # ============================================================

    if department not in EXPORT_MAPPINGS:

        raise HTTPException(
            status_code=400,
            detail="Invalid department",
        )

    # ============================================================
    # 🔹 FILTER
    # ============================================================

    metric_filter = build_metric_filter(
        department,
        metric,
    )

    if metric_filter is None:

        raise HTTPException(
            status_code=400,
            detail="Invalid metric",
        )

    # ============================================================
    # 🔹 QUERY
    # ============================================================

    rows = (
        db.query(
            CampaignSegmentBatchTransaction
        )
        .filter(
            CampaignSegmentBatchTransaction.batch_code
            == batch_code
        )
        .filter(metric_filter)
        .filter(
            CampaignSegmentBatchTransaction.is_deleted
            == False
        )
        .all()
    )

    # ============================================================
    # 🔹 CSV BUFFER
    # ============================================================

    output = io.StringIO()

    writer = csv.writer(output)

    # ============================================================
    # 🔹 HEADERS
    # ============================================================

    mappings = EXPORT_MAPPINGS[department]

    headers = [
        header
        for header, _ in mappings
    ]

    writer.writerow(headers)

    # ============================================================
    # 🔹 ROWS
    # ============================================================

    for row in rows:

        csv_row = []

        for _, field_name in mappings:

            value = getattr(
                row,
                field_name,
                "",
            )

            if value is None:
                value = ""

            csv_row.append(value)

        writer.writerow(csv_row)

    output.seek(0)

    # ============================================================
    # 🔹 FILENAME
    # ============================================================

    filename = (
        f"{batch_code}_"
        f"{department}_"
        f"{metric}.csv"
    )

    # ============================================================
    # 🔹 RESPONSE
    # ============================================================

    return StreamingResponse(

        iter([output.getvalue()]),

        media_type="text/csv",

        headers={
            "Content-Disposition":
            f"attachment; filename={filename}"
        },
    )