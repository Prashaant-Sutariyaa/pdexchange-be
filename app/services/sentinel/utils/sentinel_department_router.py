from sqlalchemy.orm import Session

from app.services.sentinel.transactions.sentinel_transaction_service import (
    upsert_transaction,
)
from app.services.sentinel.processors.sentinel_email_service import (
    process_email_row,
)

from app.services.sentinel.processors.sentinel_quality_service import (
    process_quality_row,
)

from app.services.sentinel.processors.sentinel_dbr_service import (
    process_dbr_row,
)

from app.services.sentinel.processors.sentinel_vv_service import (
    process_vv_row,
)

from app.services.sentinel.processors.sentinel_mis_service import (
    process_mis_row,
)

# ============================================================
# 🔹 PROCESS DATAOPS
# ============================================================


def process_dataops(
    db: Session,
    batch_code: str,
    row: dict,
    user_id: int,
):

    upsert_transaction(
        db=db,
        batch_code=batch_code,
        row=row,
        user_id=user_id,
    )


# ============================================================
# 🔹 PROCESS EMAIL
# ============================================================


def process_email(
    db: Session,
    batch_code: str,
    row: dict,
    user_id: int,
):

    process_email_row(
        db=db,
        row=row,
        user_id=user_id,
    )


# ============================================================
# 🔹 PROCESS QUALITY
# ============================================================


def process_quality(
    db: Session,
    batch_code: str,
    row: dict,
    user_id: int,
):

    process_quality_row(
        db=db,
        row=row,
        user_id=user_id,
    )


# ============================================================
# 🔹 PROCESS DBR
# ============================================================


def process_dbr(
    db: Session,
    batch_code: str,
    row: dict,
    user_id: int,
):

    process_dbr_row(
        db=db,
        row=row,
        user_id=user_id,
    )


# ============================================================
# 🔹 PROCESS VV
# ============================================================


def process_vv(
    db: Session,
    batch_code: str,
    row: dict,
    user_id: int,
):

    process_vv_row(
        db=db,

        row=row,

        user_id=user_id,
    )


# ============================================================
# 🔹 PROCESS MIS
# ============================================================


def process_mis(
    db: Session,
    batch_code: str,
    row: dict,
    user_id: int,
):

    process_mis_row(
        db=db,

        row=row,

        user_id=user_id,
    )


# ============================================================
# 🔹 MAIN ROUTER
# ============================================================


def process_department_row(
    db: Session,
    department: str,
    batch_code: str,
    row: dict,
    user_id: int,
):

    department = department.strip().lower()

    # ============================================================
    # 🔹 DATAOPS
    # ============================================================

    if department == "dataops":

        return process_dataops(
            db=db,
            batch_code=batch_code,
            row=row,
            user_id=user_id,
        )

    # ============================================================
    # 🔹 EMAIL
    # ============================================================

    elif department == "email":

        return process_email(
            db=db,
            batch_code=batch_code,
            row=row,
            user_id=user_id,
        )

    # ============================================================
    # 🔹 QUALITY
    # ============================================================

    elif department == "quality":

        return process_quality(
            db=db,
            batch_code=batch_code,
            row=row,
            user_id=user_id,
        )

    # ============================================================
    # 🔹 DBR
    # ============================================================

    elif department == "dbr":

        return process_dbr(
            db=db,
            batch_code=batch_code,
            row=row,
            user_id=user_id,
        )

    # ============================================================
    # 🔹 VV
    # ============================================================

    elif department == "voice verification" or department == "vv":

        return process_vv(
            db=db,
            batch_code=batch_code,
            row=row,
            user_id=user_id,
        )

    # ============================================================
    # 🔹 MIS
    # ============================================================

    elif department == "mis":

        return process_mis(
            db=db,
            batch_code=batch_code,
            row=row,
            user_id=user_id,
        )

    else:

        raise Exception(f"Unsupported department: {department}")
