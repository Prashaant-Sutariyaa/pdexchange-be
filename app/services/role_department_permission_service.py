from sqlalchemy.orm import Session
from app.models.role_department_permission import RoleDepartmentPermission


def upsert_rdp(db: Session, data, user_id: int):
    existing = db.query(RoleDepartmentPermission).filter(
        RoleDepartmentPermission.role_id == data.role_id,
        RoleDepartmentPermission.department_id == data.department_id,
        RoleDepartmentPermission.module_permission_id == data.module_permission_id
    ).first()

    # 🔥 UPDATE if exists
    if existing:
        existing.is_active = data.is_active
        existing.updated_by = user_id

        db.commit()
        db.refresh(existing)
        return existing

    # 🔥 CREATE if not exists
    obj = RoleDepartmentPermission(
        role_id=data.role_id,
        department_id=data.department_id,
        module_permission_id=data.module_permission_id,
        is_active=data.is_active,
        created_by=user_id,
        updated_by=user_id
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj