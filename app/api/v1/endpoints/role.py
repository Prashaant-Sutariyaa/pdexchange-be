from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.services.role_service import (
    create_role,
    get_roles,
    get_role,
    update_role,
    delete_role,
)

router = APIRouter(prefix="/roles", tags=["Roles"])


# 🚀 CREATE
@router.post(
    "/",
    response_model=RoleResponse,
    dependencies=[Depends(check_permission("roles", "create"))],
)
def create(
    data: RoleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    role = create_role(db, data, user.id)

    if role == "exists":
        raise HTTPException(status_code=409, detail="Role already exists")

    if role == "deleted":
        raise HTTPException(
            status_code=409, detail="Role exists but is deleted. Please restore."
        )

    return role


# 🚀 GET ALL (FULL API)
@router.get(
    "/",
    response_model=list[RoleResponse],
    dependencies=[Depends(check_permission("roles", "view"))],
)
def read_all(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_roles(db, is_active)


# 🚀 LIST API (LIGHTWEIGHT)
@router.get("/list", dependencies=[Depends(get_current_user)])  # ✅ only auth required
def role_list(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    roles = get_roles(db, is_active)

    # 🔹 return minimal data
    return [{"id": r.id, "name": r.name} for r in roles]


# 🚀 GET ONE
@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[Depends(check_permission("roles", "view"))],
)
def read_one(
    role_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    role = get_role(db, role_id)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


# 🚀 PATCH
@router.patch(
    "/{role_id}",
    response_model=RoleResponse,
    dependencies=[Depends(check_permission("roles", "edit"))],
)
def update(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    role = update_role(db, role_id, data, user.id)

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


# 🚀 DELETE
@router.delete("/{role_id}", dependencies=[Depends(check_permission("roles", "delete"))])
def delete(role_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    result = delete_role(db, role_id, user.id)

    if not result:
        raise HTTPException(status_code=404, detail="Role not found")

    return {"message": "Role deleted successfully"}
