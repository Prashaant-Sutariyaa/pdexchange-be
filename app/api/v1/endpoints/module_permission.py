from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from typing import Optional

from app.schemas.module_permission import (
    ModulePermissionCreate,
    ModulePermissionUpdate,
    ModulePermissionResponse,
)

from app.services.module_permission_service import (
    create_module_permission,
    get_module_permissions,
    get_module_permission,
    update_module_permission,
    delete_module_permission,
)

router = APIRouter(prefix="/module-permissions", tags=["Module Permissions"])


# 🚀 CREATE
@router.post("/", response_model=ModulePermissionResponse)
def create(
    data: ModulePermissionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    obj = create_module_permission(db, data, user.id)

    # 🔥 HANDLE DUPLICATES
    if obj == "exists":
        raise HTTPException(status_code=409, detail="Already exists")

    if obj == "deleted":
        raise HTTPException(
            status_code=409, detail="Record exists but is deleted. Please restore."
        )

    return obj


# 🚀 GET ALL
# 🚀 GET ALL
@router.get("/")
def read_all(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_module_permissions(
        db=db,
        search=search,
        is_active=is_active,
        page=page,
        limit=limit,
    )


# 🚀 GET ONE
@router.get("/{obj_id}", response_model=ModulePermissionResponse)
def read_one(
    obj_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    obj = get_module_permission(db, obj_id)

    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    return obj


# 🚀 UPDATE
@router.patch("/{obj_id}", response_model=ModulePermissionResponse)
def update(
    obj_id: int,
    data: ModulePermissionUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    obj = update_module_permission(db, obj_id, data, user.id)

    if obj == "duplicate":
        raise HTTPException(
            status_code=409, detail="Permission already exists for this module"
        )

    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    return obj


# 🚀 DELETE (SOFT DELETE FIX)
@router.delete("/{obj_id}")
def delete(obj_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    result = delete_module_permission(db, obj_id, user.id)  # ✅ FIX

    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted successfully"}
