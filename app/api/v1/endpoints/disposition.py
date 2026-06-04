from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user,
)

from app.core.permissions import check_permission

from app.services.disposition_service import (
    get_dispositions,
    get_disposition,
)

router = APIRouter(
    prefix="/dispositions",
    tags=["Dispositions"],
)


# ============================================================
# 🔹 GET ALL
# ============================================================
@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
)
def read_all(
    page: int | None = Query(None, ge=1),
    limit: int | None = Query(None, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return get_dispositions(
        db=db,
        page=page,
        limit=limit,
    )


# ============================================================
# 🔹 GET ONE
# ============================================================
@router.get(
    "/{disposition_id}",
    dependencies=[Depends(get_current_user)],
)
def read_one(
    disposition_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    disposition = get_disposition(
        db,
        disposition_id,
    )

    if not disposition:
        raise HTTPException(
            status_code=404,
            detail="Disposition not found",
        )

    return disposition
