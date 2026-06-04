import os

from datetime import datetime

from app.utils.csv_helper import (
    read_csv_file,
    write_invalid_csv,
)

INVALID_PATH = "storage/sentinel/failed_upload"


# ============================================================
# 🔹 NORMALIZE KEYS
# ============================================================


def normalize_row(
    row: dict,
):

    return {
        "batch_code": row.get("Batch ID"),
        "dataops_agent": row.get("DataOps Agent"),
        "vendor_code": row.get("Vendor Code"),
        "salutation": row.get("Salutations"),
        "first_name": row.get("First Name"),
        "last_name": row.get("Last Name"),
        "email": row.get("Work Email"),
        "tal_company_name": row.get("TAL Company Name"),
        "li_company_name": row.get("Linkedin Company Name"),
        "domain": row.get("Domain"),
        "job_title": row.get("Job Title"),
        "job_level": row.get("Job Level"),
        "job_department": row.get("Job Department"),
        "work_phone": row.get("WorkPhone"),
        "headquarter_phone": row.get("Headquarter Phone"),
        "contact_li_profile": row.get("Contact Linkedin Profile"),
        "address1": row.get("Address 1"),
        "address2": row.get("Address 2"),
        "city": row.get("City"),
        "state": row.get("State"),
        "zip_code": row.get("Zip Code"),
        "country": row.get("Country"),
        "industry": row.get("Industry"),
        "sub_industry": row.get("Sub Industry"),
        "sic_code": row.get("SIC Code"),
        "naics_code": row.get("NAICS Code"),
        "employee_count": row.get("Employees Count"),
        "employee_range": row.get("Employees Range"),
        "revenue_count": row.get("Revenue Count"),
        "revenue_range": row.get("Revenue Range ($)"),
        "company_li_profile": row.get("Company Linkedin Profile"),
        "source": row.get("Source"),
        "installbase_technology": row.get("Install Base Technology"),
        "email_validation_status": (
            "Valid"
            if str(row.get("Email Validation Status", "")).strip().lower()
            in ["ok", "valid", "catch-all", "catch_all", "apollo verify", "verified"]
            else "Invalid"
        ),
        # OPTIONAL
        "campaign_code": row.get("Campaign Code"),
        "segment_code": row.get("Segment Code"),
    }


# ============================================================
# 🔹 NORMALIZE EMAIL ROW
# ============================================================


def normalize_email_row(
    row: dict,
):

    return {
        "batch_code": row.get("Batch ID"),
        "email_agent": row.get("Email Agent"),
        "email": row.get("Work Email"),
        "email_status": row.get("Email Status"),
        "email_reason": row.get("Email Reason"),
        "asset1": row.get("Asset1"),
        "asset2": row.get("Asset2"),
        "ip_address": row.get("IP Address"),
        "email_time_tool": row.get("Email_TimeStamp"),
    }


# ============================================================
# 🔹 NORMALIZE QUALITY ROW
# ============================================================


def normalize_quality_row(
    row: dict,
):

    return {
        "batch_code": row.get("Batch ID"),
        "quality_agent": row.get("Quality Agent"),
        "quality_status": row.get("Quality Status"),
        "quality_reason": row.get("Quality Reason"),
        "work_experience": row.get("Work Experience"),
        "activity": row.get("Activity"),
        "comments": row.get("Comments"),
        "email": row.get("Work Email"),
    }


# ============================================================
# 🔹 NORMALIZE DBR ROW
# ============================================================


def normalize_dbr_row(
    row: dict,
):

    return {
        "batch_code": row.get("Batch ID"),
        "dbr_agent": row.get("DBR Agent"),
        "dbr_status": row.get("DBR Status"),
        "email": row.get("Work Email"),
    }


# ============================================================
# 🔹 NORMALIZE VV ROW
# ============================================================


def normalize_vv_row(
    row: dict,
):

    return {
        "batch_code": row.get("Batch ID"),
        "vv_agent": row.get("VV Agent"),
        "email": row.get("Work Email"),
        "vv_number": row.get("VV Number"),
        "vv_disposition": row.get("VV Disposition"),
    }


# ============================================================
# 🔹 NORMALIZE MIS ROW
# ============================================================


def normalize_mis_row(
    row: dict,
):

    return {
        "batch_code": row.get("Batch ID"),
        "mis_agent": row.get("MIS Agent"),
        "email": row.get("Work Email"),
        "mis_status": row.get("MIS Status"),
        "mis_reason": row.get("MIS Reason"),
    }


# ============================================================
# 🔹 PROCESS CSV
# ============================================================


def process_csv_file(
    file_path: str,
    department: str,
):

    rows = read_csv_file(file_path)

    total_rows = len(rows)

    valid_rows = []

    invalid_rows = []

    # ============================================================
    # 🔹 PROCESS ROWS
    # ============================================================

    for raw_row in rows:

        # ============================================================
        # 🔹 DATAOPS
        # ============================================================

        if department.lower() == "dataops":

            row = normalize_row(raw_row)

            email = (row.get("email") or "").strip()

            if not email:

                row["system_reason"] = "Email is required"

                invalid_rows.append(row)

                continue

        # ============================================================
        # 🔹 EMAIL
        # ============================================================

        elif department.lower() == "email":

            row = normalize_email_row(raw_row)

            batch_code = (row.get("batch_code") or "").strip()

            email = (row.get("email") or "").strip()

            if not batch_code:

                row["system_reason"] = "Batch ID is required"

                invalid_rows.append(row)

                continue

            if not email:

                row["system_reason"] = "Work Email is required"

                invalid_rows.append(row)

                continue

        # ============================================================
        # 🔹 QUALITY
        # ============================================================

        elif department.lower() == "quality":

            row = normalize_quality_row(raw_row)

            batch_code = (row.get("batch_code") or "").strip()

            email = (row.get("email") or "").strip()

            if not batch_code:

                row["system_reason"] = "Batch ID is required"

                invalid_rows.append(row)

                continue

            if not email:

                row["system_reason"] = "Work Email is required"

                invalid_rows.append(row)

                continue

        # ============================================================
        # 🔹 DBR
        # ============================================================

        elif department.lower() == "dbr":

            row = normalize_dbr_row(raw_row)

            batch_code = (row.get("batch_code") or "").strip()

            email = (row.get("email") or "").strip()

            if not batch_code:

                row["system_reason"] = "Batch ID is required"

                invalid_rows.append(row)

                continue

            if not email:

                row["system_reason"] = "Work Email is required"

                invalid_rows.append(row)

                continue

        # ============================================================
        # 🔹 VV
        # ============================================================

        elif department.lower() == "voice verification" or department.lower() == "vv":

            row = normalize_vv_row(raw_row)

            batch_code = (row.get("batch_code") or "").strip()

            email = (row.get("email") or "").strip()

            if not batch_code:

                row["system_reason"] = "Batch ID is required"

                invalid_rows.append(row)

                continue

            if not email:

                row["system_reason"] = "Work Email is required"

                invalid_rows.append(row)

                continue

        # ============================================================
        # 🔹 MIS
        # ============================================================

        elif department.lower() == "mis":

            row = normalize_mis_row(raw_row)

            batch_code = (row.get("batch_code") or "").strip()

            email = (row.get("email") or "").strip()

            if not batch_code:

                row["system_reason"] = "Batch ID is required"

                invalid_rows.append(row)

                continue

            if not email:

                row["system_reason"] = "Work Email is required"

                invalid_rows.append(row)

                continue

        else:

            row = raw_row

        valid_rows.append(row)

    return {
        "total_rows": total_rows,
        "valid_rows": len(valid_rows),
        "invalid_rows": len(invalid_rows),
        "valid_data": valid_rows,
        "invalid_data": invalid_rows,
    }
