from sqlalchemy.orm import Session

from app.models.disposition import Disposition


# ============================================================
# 🔹 FORMAT
# ============================================================
def format_disposition(d: Disposition):
    return {
        "id": d.id,
        "disposition_code": d.disposition_code,
        "call_disposition": d.call_disposition,
        "status": d.status,
        "sentinel_status": d.sentinel_status,
        "churnable": d.churnable,
    }


# ============================================================
# 🔹 GET ALL
# ============================================================
def get_dispositions(
    db: Session,
    page: int | None = None,
    limit: int | None = None,
):

    query = db.query(Disposition).filter(Disposition.is_deleted == False)

    total = query.count()

    # ========================================================
    # 🔹 PAGINATED
    # ========================================================

    if page and limit:

        offset = (page - 1) * limit

        dispositions = (
            query.order_by(Disposition.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    # ========================================================
    # 🔹 RETURN ALL
    # ========================================================

    else:

        dispositions = query.order_by(Disposition.created_at.desc()).all()

    return {
        "data": [format_disposition(d) for d in dispositions],
        "page": page,
        "limit": limit,
        "total": total,
    }


# ============================================================
# 🔹 GET ONE
# ============================================================
def get_disposition(
    db: Session,
    disposition_id: int,
):

    disposition = (
        db.query(Disposition)
        .filter(
            Disposition.id == disposition_id,
            Disposition.is_deleted == False,
        )
        .first()
    )

    if not disposition:
        return None

    return format_disposition(disposition)
