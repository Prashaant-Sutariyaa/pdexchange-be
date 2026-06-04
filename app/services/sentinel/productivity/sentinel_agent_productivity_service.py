from sqlalchemy.orm import Session

from app.models.sentinel_agent_productivity import (
    SentinelAgentProductivity,
)


# ============================================================
# 🔹 FORMAT
# ============================================================
def format_agent_productivity(p: SentinelAgentProductivity):
    return {
        "id": p.id,

        "agent_id": p.agent_id,

        "agent_email": p.agent_email,

        "department": p.department,

        "campaign_code": p.campaign_code,
        "segment_code": p.segment_code,
        "batch_code": p.batch_code,

        "total_rows": p.total_rows,
        "valid_rows": p.valid_rows,
        "invalid_rows": p.invalid_rows,

        "work_date": (
            str(p.work_date)
            if p.work_date
            else None
        ),

        "derived_from": p.derived_from,

        "created_at": (
            p.created_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if p.created_at
            else None
        ),
    }


# ============================================================
# 🔹 GET ALL
# ============================================================
def get_agent_productivity_list(db: Session):

    productivity = (
        db.query(SentinelAgentProductivity)
        .order_by(SentinelAgentProductivity.created_at.desc())
        .all()
    )

    return [format_agent_productivity(p) for p in productivity]


# ============================================================
# 🔹 GET ONE
# ============================================================
def get_agent_productivity(db: Session, productivity_id: int):

    productivity = (
        db.query(SentinelAgentProductivity)
        .filter(SentinelAgentProductivity.id == productivity_id)
        .first()
    )

    if not productivity:
        return None

    return format_agent_productivity(productivity)