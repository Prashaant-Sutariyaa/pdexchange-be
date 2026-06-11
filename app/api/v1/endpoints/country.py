from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.services.country_service import (
    get_countries,
    get_country,
)

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
)


# 🔹 GET ALL COUNTRIES
@router.get(
    "/",
)
def read_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_countries(db)


# 🔹 GET ONE COUNTRY
@router.get(
    "/{country_id}"
)
def read_one(
    country_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    country = get_country(
        db,
        country_id,
    )

    if not country:
        raise HTTPException(
            status_code=404,
            detail="Country not found",
        )

    return country