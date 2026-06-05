from sqlalchemy.orm import Session

from app.models.module_permission import ModulePermission
from app.models.role_permission import RolePermission
from app.models.user_permission import UserPermission


def get_user_permissions(db: Session, user):
    result = {}

    # ============================================================
    # GET ALL MODULE PERMISSIONS
    # ============================================================

    module_perms = (
        db.query(ModulePermission).filter(ModulePermission.is_deleted == False).all()
    )

    # ============================================================
    # ROLE PERMISSIONS
    # ============================================================

    role_permissions = (
        db.query(RolePermission).filter(RolePermission.role_id == user.role_id).all()
    )

    role_perm_map = {rp.module_permission_id: rp.is_active for rp in role_permissions}

    # ============================================================
    # BUILD BASE ACCESS MAP
    # ============================================================

    temp = {}

    for mp in module_perms:
        temp[mp.id] = role_perm_map.get(mp.id, False)

    # ============================================================
    # USER OVERRIDES
    # ============================================================

    user_permissions = (
        db.query(UserPermission).filter(UserPermission.user_id == user.id).all()
    )

    for up in user_permissions:
        temp[up.module_permission_id] = up.is_active

    # ============================================================
    # CONVERT TO RESPONSE FORMAT
    # ============================================================

    for mp in module_perms:

        if temp.get(mp.id):

            module = mp.module_name
            permission = mp.permission_name

            if module not in result:
                result[module] = []

            result[module].append(permission)

    return result
