from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)
from app.services.department_service import (
    create_department,
    get_departments,
    get_department,
    update_department,
    delete_department
)

router = APIRouter(prefix="/departments", tags=["Departments"])


# 🚀 CREATE
@router.post(
    "/",
    response_model=DepartmentResponse,
    dependencies=[Depends(check_permission("department", "create"))]
)
def create(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    dept = create_department(db, data, user.id)

    if dept == "exists":
        raise HTTPException(status_code=409, detail="Department already exists")

    if dept == "deleted":
        raise HTTPException(
            status_code=409,
            detail="Department exists but is deleted. Please restore."
        )

    return dept


# 🚀 GET ALL (FULL API)
@router.get(
    "/",
    response_model=list[DepartmentResponse],
    dependencies=[Depends(check_permission("department", "view"))]
)
def read_all(
    is_active: Optional[bool] = None,
    is_deleted: Optional[bool] = False,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_departments(db, is_active, is_deleted)


# 🚀 LIST API (LIGHTWEIGHT)
@router.get(
    "/list",
    dependencies=[Depends(get_current_user)]   # ✅ only auth required
)
def department_list(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    departments = get_departments(db, is_active, False)

    return [
        {
            "id": d.id,
            "name": d.name
        }
        for d in departments
    ]


# 🚀 GET ONE
@router.get(
    "/{dept_id}",
    response_model=DepartmentResponse,
    dependencies=[Depends(check_permission("department", "view"))]
)
def read_one(
    dept_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    dept = get_department(db, dept_id)

    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    return dept


# 🚀 PATCH
@router.patch(
    "/{dept_id}",
    response_model=DepartmentResponse,
    dependencies=[Depends(check_permission("department", "edit"))]
)
def update(
    dept_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    dept = update_department(db, dept_id, data, user.id)

    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    return dept


# 🚀 DELETE
@router.delete(
    "/{dept_id}",
    dependencies=[Depends(check_permission("department", "delete"))]
)
def delete(
    dept_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    result = delete_department(db, dept_id, user.id)

    if not result:
        raise HTTPException(status_code=404, detail="Department not found")

    return {"message": "Department deleted successfully"}