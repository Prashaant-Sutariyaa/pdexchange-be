from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.module_permission import ModulePermission
from sqlalchemy import or_, func


# 🔹 CREATE
def create_module_permission(db: Session, data, user_id: int):
    module = data.module_name.lower()  # ✅ normalize
    permission = data.permission_name.lower()  # ✅ normalize

    existing = (
        db.query(ModulePermission)
        .filter(
            func.lower(ModulePermission.module_name) == module,
            func.lower(ModulePermission.permission_name) == permission,
        )
        .first()
    )

    if existing:
        if hasattr(existing, "is_deleted") and existing.is_deleted:
            return "deleted"
        return "exists"

    obj = ModulePermission(
        module_name=module,
        menu_name=data.menu_name,
        permission_name=permission,
        description=data.description,
        is_active=data.is_active,
        created_by=user_id,
        updated_by=user_id,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# 🔹 GET ALL (listing)
# 🔹 GET ALL WITH PAGINATION + SEARCH
def get_module_permissions(
    db: Session,
    search: str = None,
    is_active: bool = None,
    page: int = 1,
    limit: int = 20,
):

    query = db.query(ModulePermission)

    # ============================================================
    # 🔥 ALWAYS HIDE DELETED RECORDS
    # ============================================================
    query = query.filter(ModulePermission.is_deleted == False)

    # ============================================================
    # 🔥 ACTIVE FILTER
    # ============================================================
    if is_active is not None:
        query = query.filter(ModulePermission.is_active == is_active)

    # ============================================================
    # 🔥 GLOBAL SEARCH
    # ============================================================
    if search:
        query = query.filter(
            or_(
                ModulePermission.module_name.ilike(f"%{search}%"),
                ModulePermission.menu_name.ilike(f"%{search}%"),
                ModulePermission.permission_name.ilike(f"%{search}%"),
            )
        )

    # ============================================================
    # 🔢 TOTAL COUNT
    # ============================================================
    total = query.count()

    # ============================================================
    # 🔢 PAGINATION (OPTIONAL)
    # ============================================================
    if page and limit:

        offset = (page - 1) * limit

        data = (
            query.order_by(ModulePermission.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "data": data,
            "page": page,
            "limit": limit,
            "total": total,
        }

    # ============================================================
    # 🔥 RETURN ALL
    # ============================================================
    data = query.order_by(ModulePermission.created_at.desc()).all()

    return data


# 🔹 GET ONE
def get_module_permission(db: Session, obj_id: int):
    return (
        db.query(ModulePermission)
        .filter(
            ModulePermission.id == obj_id,
            ModulePermission.is_deleted == False,  # ✅ ADD
        )
        .first()
    )


# 🔹 UPDATE
def update_module_permission(db: Session, obj_id: int, data, user_id: int):
    obj = (
        db.query(ModulePermission)
        .filter(
            ModulePermission.id == obj_id,
            ModulePermission.is_deleted == False,  # ✅ ADD
        )
        .first()
    )

    if not obj:
        return None

    # 🔥 Normalize new values
    new_module = (
        data.module_name.lower() if data.module_name is not None else obj.module_name
    )
    new_permission = (
        data.permission_name.lower()
        if data.permission_name is not None
        else obj.permission_name
    )

    # 🔥 Duplicate check (case-insensitive)
    existing = (
        db.query(ModulePermission)
        .filter(
            func.lower(ModulePermission.module_name) == new_module,
            func.lower(ModulePermission.permission_name) == new_permission,
            ModulePermission.id != obj_id,
        )
        .first()
    )

    if existing:
        return "duplicate"

    # 🔄 Update fields
    if data.module_name is not None:
        obj.module_name = new_module

    if data.menu_name is not None:
        obj.menu_name = data.menu_name

    if data.permission_name is not None:
        obj.permission_name = new_permission

    if data.description is not None:
        obj.description = data.description

    if data.is_active is not None:
        obj.is_active = data.is_active

    obj.updated_by = user_id

    db.commit()
    db.refresh(obj)

    return obj


# 🔹 DELETE (SOFT DELETE 🔥)
def delete_module_permission(db: Session, obj_id: int, user_id: int):
    obj = get_module_permission(db, obj_id)

    if not obj:
        return None

    # 🔹 Soft delete: marks record as deleted and sets is_active=False (if present)
    obj.soft_delete()
    obj.updated_by = user_id

    db.commit()

    return True
