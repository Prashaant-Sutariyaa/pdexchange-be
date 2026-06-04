from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user

from app.schemas.role_department_permission import RDPUpset
from app.services.role_department_permission_service import upsert_rdp
from app.models.role_department_permission import RoleDepartmentPermission

router = APIRouter(
    prefix="/role-department-permissions",
    tags=["Role Department Permissions"]
)



@router.get("/")
def read_all(
    role_id: int,
    department_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(RoleDepartmentPermission).filter(
        RoleDepartmentPermission.role_id == role_id,
        RoleDepartmentPermission.department_id == department_id
    ).all()


# 🚀 UPSERT (CREATE + UPDATE)
@router.post("/upsert")
def upsert(
    data: RDPUpset,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return upsert_rdp(db, data, user.id)