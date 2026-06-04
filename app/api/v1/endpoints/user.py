from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import (
    create_user,
    get_users,
    get_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


# 🚀 PROFILE
@router.get("/profile", response_model=UserResponse)
def get_profile(user=Depends(get_current_user)):
    return user


# 🚀 CREATE
@router.post(
    "/",
    response_model=UserResponse,
    dependencies=[Depends(check_permission("users", "create"))],
)
def create(
    data: UserCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    obj = create_user(db, data, user.id)

    if obj == "exists":
        raise HTTPException(status_code=409, detail="User already exists")

    if obj == "deleted":
        raise HTTPException(
            status_code=409, detail="User exists but is deleted. Please restore user."
        )

    return obj


# 🚀 GET ALL / PAGINATED
@router.get(
    "/",
    dependencies=[Depends(check_permission("users", "view"))],
)
def read_all(
    is_active: Optional[bool] = None,
    is_deleted: Optional[bool] = False,
    page: Optional[int] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_users(
        db=db,
        is_active=is_active,
        is_deleted=is_deleted,
        page=page,
        limit=limit,
    )


# 🚀 LIST API (LIGHTWEIGHT)
@router.get("/list", dependencies=[Depends(get_current_user)])  # ✅ only auth required
def user_list(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    response = get_users(
        db=db,
        is_active=is_active,
        is_deleted=False,
    )

    users = response["data"]

    return [
        {
            "id": u.id,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
        }
        for u in users
    ]


# 🚀 GET ONE
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(check_permission("users", "view"))],
)
def read_one(
    user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    obj = get_user(db, user_id)

    if not obj:
        raise HTTPException(status_code=404, detail="User not found")

    return obj


# 🚀 UPDATE
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(check_permission("users", "edit"))],
)
def update(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    obj = update_user(db, user_id, data, user.id)

    if not obj:
        raise HTTPException(status_code=404, detail="User not found")

    return obj


# 🚀 DELETE (SOFT)
@router.delete(
    "/{user_id}", dependencies=[Depends(check_permission("users", "delete"))]
)
def delete(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    result = delete_user(db, user_id, user.id)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}
