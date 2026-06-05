from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user

from app.schemas.role_permission import RolePermissionUpsert
from app.services.role_permission_service import upsert_role_permission
from app.models.role_permission import RolePermission

router = APIRouter(
    prefix="/role-permissions",
    tags=["Role Permissions"]
)


@router.get("/")
def read_all(
    role_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == role_id
        )
        .all()
    )


# 🚀 UPSERT (CREATE + UPDATE)
@router.post("/upsert")
def upsert(
    data: RolePermissionUpsert,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return upsert_role_permission(
        db,
        data,
        user.id
    )