from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.schemas.user_permission import UserPermissionUpsert
from app.services.user_permission_service import (
    upsert_user_permission,
    get_user_permissions,
    delete_user_permission
)

router = APIRouter(
    prefix="/user-permissions",
    tags=["User Permissions"]
)


# 🚀 UPSERT (ENABLE)
@router.post("/upsert")
def upsert(
    data: UserPermissionUpsert,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return upsert_user_permission(db, data, current_user.id)


# 🚀 GET (for UI)
@router.get("/")
def read_all(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_user_permissions(db, user_id)


# 🚀 DELETE (DISABLE / REMOVE OVERRIDE)
@router.delete("/")
def delete_permission(
    user_id: int,
    module_permission_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = delete_user_permission(db, user_id, module_permission_id)

    if not result:
        raise HTTPException(status_code=404, detail="Permission not found")

    return {"message": "Permission removed successfully"}