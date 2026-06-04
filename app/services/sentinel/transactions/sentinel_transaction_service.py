from datetime import datetime

from sqlalchemy import text
import hashlib
from sqlalchemy.orm import Session

# ============================================================
# 🔹 DATAOPS UPSERT
# ============================================================


def upsert_transaction(
    db: Session,
    batch_code: str,
    row: dict,
    user_id: int,
):

    query = text("""
        INSERT INTO campaign_segment_batch_transactions (
            batch_code,

            email,
            email_hash,

            vendor_code,

            salutation,

            first_name,
            last_name,

            tal_company_name,
            li_company_name,

            domain,

            job_title,
            job_level,
            job_department,

            work_phone,
            headquarter_phone,

            contact_li_profile,

            address1,
            address2,

            city,
            state,
            zip_code,
            country,

            industry,
            sub_industry,

            sic_code,
            naics_code,

            employee_count,
            employee_range,

            revenue_count,
            revenue_range,

            company_li_profile,

            source,

            installbase_technology,

            email_validation_status,

            dataops_agent,
            dataops_timestamp,

            created_at,
            created_by,

            updated_at,
            updated_by
        )
        VALUES (
            :batch_code,

            :email,
            :email_hash,

            :vendor_code,

            :salutation,

            :first_name,
            :last_name,

            :tal_company_name,
            :li_company_name,

            :domain,

            :job_title,
            :job_level,
            :job_department,

            :work_phone,
            :headquarter_phone,

            :contact_li_profile,

            :address1,
            :address2,

            :city,
            :state,
            :zip_code,
            :country,

            :industry,
            :sub_industry,

            :sic_code,
            :naics_code,

            :employee_count,
            :employee_range,

            :revenue_count,
            :revenue_range,

            :company_li_profile,

            :source,

            :installbase_technology,

            :email_validation_status,

            :dataops_agent,
            :dataops_timestamp,

            :created_at,
            :created_by,

            :updated_at,
            :updated_by
        )
        ON CONFLICT (batch_code, email)
        DO UPDATE SET

            vendor_code = EXCLUDED.vendor_code,

            salutation = EXCLUDED.salutation,

            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,

            tal_company_name = EXCLUDED.tal_company_name,
            li_company_name = EXCLUDED.li_company_name,

            domain = EXCLUDED.domain,

            job_title = EXCLUDED.job_title,
            job_level = EXCLUDED.job_level,
            job_department = EXCLUDED.job_department,

            work_phone = EXCLUDED.work_phone,
            headquarter_phone = EXCLUDED.headquarter_phone,

            contact_li_profile = EXCLUDED.contact_li_profile,

            address1 = EXCLUDED.address1,
            address2 = EXCLUDED.address2,

            city = EXCLUDED.city,
            state = EXCLUDED.state,
            zip_code = EXCLUDED.zip_code,
            country = EXCLUDED.country,

            industry = EXCLUDED.industry,
            sub_industry = EXCLUDED.sub_industry,

            sic_code = EXCLUDED.sic_code,
            naics_code = EXCLUDED.naics_code,

            employee_count = EXCLUDED.employee_count,
            employee_range = EXCLUDED.employee_range,

            revenue_count = EXCLUDED.revenue_count,
            revenue_range = EXCLUDED.revenue_range,

            company_li_profile = EXCLUDED.company_li_profile,

            source = EXCLUDED.source,

            installbase_technology = EXCLUDED.installbase_technology,

            email_validation_status = EXCLUDED.email_validation_status,

            dataops_agent = EXCLUDED.dataops_agent,
            dataops_timestamp = EXCLUDED.dataops_timestamp,

            updated_at = EXCLUDED.updated_at,
            updated_by = EXCLUDED.updated_by
    """)

    db.execute(
        query,
        {
            "batch_code": batch_code,
            "email": row.get("email"),
            "email_hash": hashlib.md5(
                str(row.get("email", "")).strip().lower().encode()
            ).hexdigest(),
            "vendor_code": row.get("vendor_code"),
            "salutation": row.get("salutation"),
            "first_name": row.get("first_name"),
            "last_name": row.get("last_name"),
            "tal_company_name": row.get("tal_company_name"),
            "li_company_name": row.get("li_company_name"),
            "domain": row.get("domain"),
            "job_title": row.get("job_title"),
            "job_level": row.get("job_level"),
            "job_department": row.get("job_department"),
            "work_phone": row.get("work_phone"),
            "headquarter_phone": row.get("headquarter_phone"),
            "contact_li_profile": row.get("contact_li_profile"),
            "address1": row.get("address1"),
            "address2": row.get("address2"),
            "city": row.get("city"),
            "state": row.get("state"),
            "zip_code": row.get("zip_code"),
            "country": row.get("country"),
            "industry": row.get("industry"),
            "sub_industry": row.get("sub_industry"),
            "sic_code": row.get("sic_code"),
            "naics_code": row.get("naics_code"),
            "employee_count": row.get("employee_count"),
            "employee_range": row.get("employee_range"),
            "revenue_count": row.get("revenue_count"),
            "revenue_range": row.get("revenue_range"),
            "company_li_profile": row.get("company_li_profile"),
            "source": row.get("source"),
            "installbase_technology": row.get("installbase_technology"),
            "email_validation_status": row.get(
                "email_validation_status",
                "Valid",
            ),
            "dataops_agent": row.get("dataops_agent"),
            "dataops_timestamp": datetime.utcnow(),
            "created_at": datetime.utcnow(),
            "created_by": user_id,
            "updated_at": datetime.utcnow(),
            "updated_by": user_id,
        },
    )
