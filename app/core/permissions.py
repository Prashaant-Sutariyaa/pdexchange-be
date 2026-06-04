# from fastapi import Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy import func

# from app.core.dependencies import get_db, get_current_user

# from app.models.module_permission import ModulePermission
# from app.models.role_department_permission import RoleDepartmentPermission
# from app.models.user_permission import UserPermission
# from app.schemas import user


# def check_permission(module_name: str, permission_name: str):
#     def permission_dependency(
#         db: Session = Depends(get_db),
#         user=Depends(get_current_user)
#     ):
#         # 🔹 Normalize
#         module = module_name.lower()
#         permission = permission_name.lower()

#         # 🔹 STEP 1: Get module_permission_id
#         module_perm = db.query(ModulePermission).filter(
#             func.lower(ModulePermission.module_name) == module,
#             func.lower(ModulePermission.permission_name) == permission,
#             ModulePermission.is_deleted == False
#         ).first()

#         if not module_perm:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Permission not configured"
#             )

#         # 🔹 STEP 2: Check USER PERMISSION (override)
#         user_perm = db.query(UserPermission).filter(
#             UserPermission.user_id == user.id,
#             UserPermission.module_permission_id == module_perm.id
#         ).first()

#         if user_perm:
#             return True

#         if user_perm:
#             if user_perm.is_active:
#                 return True
#             else:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="Access denied (user override)"
#                 )

#         # 🔹 STEP 3: Check ROLE + DEPARTMENT (RDP)
#         rdp = db.query(RoleDepartmentPermission).filter(
#             RoleDepartmentPermission.role_id == user.role_id,
#             RoleDepartmentPermission.department_id == user.department_id,
#             RoleDepartmentPermission.module_permission_id == module_perm.id
#         ).first()

#         if rdp and rdp.is_active:
#             return True

#         # 🔹 STEP 4: DENY
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Access denied"
#         )

#     return permission_dependency

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.dependencies import get_db, get_current_user

from app.models.module_permission import ModulePermission
from app.models.role_department_permission import RoleDepartmentPermission
from app.models.user_permission import UserPermission


def check_permission(module_name: str, permission_name: str):
    def permission_dependency(
        db: Session = Depends(get_db), user=Depends(get_current_user)
    ):
        # 🔹 Normalize input
        module = module_name.lower()
        permission = permission_name.lower()

        # 🔹 STEP 1: Check module_permission exists
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

        # 🔹 STEP 2: User Override (Hard Delete Strategy)
        # - If record exists → ALLOW
        # - If not exists → fallback to role/department
        # - No deny override in this design
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

        # 🔹 STEP 3: Role + Department Permission
        rdp = (
            db.query(RoleDepartmentPermission)
            .filter(
                RoleDepartmentPermission.role_id == user.role_id,
                RoleDepartmentPermission.department_id == user.department_id,
                RoleDepartmentPermission.module_permission_id == module_perm.id,
            )
            .first()
        )

        if rdp and rdp.is_active:
            return True

        # 🔹 STEP 4: Access Denied
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: You do not have permission to access this feature.",
        )

    return permission_dependency
