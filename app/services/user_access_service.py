from sqlalchemy.orm import Session

from app.models.module_permission import ModulePermission
from app.models.role_department_permission import RoleDepartmentPermission
from app.models.user_permission import UserPermission


def get_user_permissions(db: Session, user):
    result = {}

    # 🔹 Get all module permissions
    module_perms = db.query(ModulePermission).filter(
        ModulePermission.is_deleted == False
    ).all()

    # 🔹 RDP base permissions
    rdp_list = db.query(RoleDepartmentPermission).filter(
        RoleDepartmentPermission.role_id == user.role_id,
        RoleDepartmentPermission.department_id == user.department_id
    ).all()

    rdp_map = {r.module_permission_id: r.is_active for r in rdp_list}

    # 🔹 Start building permission map
    temp = {}

    for mp in module_perms:
        key = mp.id
        temp[key] = rdp_map.get(key, False)

    # 🔹 Apply USER overrides
    user_perms = db.query(UserPermission).filter(
        UserPermission.user_id == user.id
    ).all()

    for up in user_perms:
        temp[up.module_permission_id] = up.is_active   # override

    # 🔹 Convert to module → [permissions]
    for mp in module_perms:
        if temp.get(mp.id):  # only allowed
            module = mp.module_name
            perm = mp.permission_name

            if module not in result:
                result[module] = []

            result[module].append(perm)

    return result