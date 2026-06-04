from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
)

from app.core.permissions import (
    check_permission,
)

from app.services.sentinel.exports.sentinel_export_service import (
    export_metric_csv,
)
from app.models.department import Department

router = APIRouter(
    prefix="/sentinel/export",
    tags=["Sentinel Export"],
)


# ============================================================
# 🔹 EXPORT CSV
# ============================================================


@router.get(
    "/",
    dependencies=[
        Depends(
            check_permission(
                "sentinel",
                "view",
            )
        )
    ],
)
def export_csv(
    batch_code: str,
    metric: str,
    department: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    department_obj = (
        db.query(Department).filter(Department.id == user.department_id).first()
    )

    return export_metric_csv(
        db=db,
        batch_code=batch_code,
        department=department,
        metric=metric,
        user_department=department_obj.name,
    )
