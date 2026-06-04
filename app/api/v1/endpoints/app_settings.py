from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user

from app.schemas.app_settings import (
    AppSettingCreate,
    AppSettingUpdate,
    AppSettingResponse
)

from app.services.app_settings_service import (
    create_setting,
    get_settings,
    get_setting,
    update_setting,
    delete_setting
)

router = APIRouter(prefix="/app-settings", tags=["App Settings"])


# CREATE
@router.post("/", response_model=AppSettingResponse)
def create(data: AppSettingCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = create_setting(db, data, user.id)

    if obj == "exists":
        raise HTTPException(status_code=409, detail="Setting already exists")

    if obj == "deleted":
        raise HTTPException(status_code=409, detail="Setting exists but deleted")

    return obj


# GET ALL
@router.get("/", response_model=list[AppSettingResponse])
def read_all(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_settings(db)


# GET ONE
@router.get("/{key}", response_model=AppSettingResponse)
def read_one(key: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = get_setting(db, key)

    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    return obj


# UPDATE
@router.patch("/{key}", response_model=AppSettingResponse)
def update(key: str, data: AppSettingUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = update_setting(db, key, data, user.id)

    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    return obj


# DELETE
@router.delete("/{key}")
def delete(key: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    result = delete_setting(db, key, user.id)

    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted successfully"}