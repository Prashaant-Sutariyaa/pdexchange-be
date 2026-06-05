from sqlalchemy.orm import Session

from app.models.role_permission import RolePermission


def upsert_role_permission(
    db: Session,
    data,
    user_id: int
):
    existing = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id == data.role_id,
            RolePermission.module_permission_id
            == data.module_permission_id,
        )
        .first()
    )

    # UPDATE
    if existing:
        existing.is_active = data.is_active
        existing.updated_by = user_id

        db.commit()
        db.refresh(existing)

        return existing

    # CREATE
    obj = RolePermission(
        role_id=data.role_id,
        module_permission_id=data.module_permission_id,
        is_active=data.is_active,
        created_by=user_id,
        updated_by=user_id,
    )

    db.add(obj)

    db.commit()
    db.refresh(obj)

    return obj