from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.dependencies import get_db, get_current_user

from app.models.module_permission import ModulePermission
from app.models.role_permission import RolePermission
from app.models.user_permission import UserPermission


def check_permission(module_name: str, permission_name: str):
    def permission_dependency(
        db: Session = Depends(get_db), user=Depends(get_current_user)
    ):
        # 🔹 Normalize input
        module = module_name.lower()
        permission = permission_name.lower()

        # 🔹 STEP 1: Check module permission exists
        module_perm = (
            db.query(ModulePermission)
            .filter(
                func.lower(ModulePermission.module_name) == module,
                func.lower(ModulePermission.permission_name) == permission,
                ModulePermission.is_deleted == False,
            )
            .first()
        )

        if not module_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_name}' for module '{module_name}' is not configured",
            )

        # ====================================================
        # USER OVERRIDE
        # ====================================================

        user_perm = (
            db.query(UserPermission)
            .filter(
                UserPermission.user_id == user.id,
                UserPermission.module_permission_id == module_perm.id,
            )
            .first()
        )

        if user_perm:
            return True

        # ====================================================
        # ROLE PERMISSION
        # ====================================================

        role_perm = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_id == user.role_id,
                RolePermission.module_permission_id == module_perm.id,
            )
            .first()
        )

        if role_perm and role_perm.is_active:
            return True

        # ====================================================
        # ACCESS DENIED
        # ====================================================

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not have permission to access this feature.",
        )

    return permission_dependency
