from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.role import Role
from app.services.audit_log_service import create_audit_log


# CREATE
def create_role(db: Session, data, user_id: int):
    name = data.name.lower()  # ✅ normalize

    existing = (
        db.query(Role)
        .filter(func.lower(Role.name) == name)  # ✅ CASE INSENSITIVE CHECK
        .first()
    )

    if existing:
        if existing.is_deleted:
            return "deleted"
        return "exists"

    role = Role(name=name, created_by=user_id, updated_by=user_id)

    try:
        db.add(role)
        db.commit()
        db.refresh(role)

        create_audit_log(
            db,
            user_id=user_id,
            action="create",
            module="role",
            record_id=role.id,
            new_data={"name": role.name},
        )

        db.commit()

        return role

    except Exception:
        db.rollback()
        return "exists"


# GET ALL
def get_roles(db: Session, is_active: bool = True):
    query = db.query(Role).filter(Role.is_deleted == False)

    # 🔹 optional filter
    if is_active is not None:
        query = query.filter(Role.is_active == is_active)

    return query.order_by(Role.created_at.desc()).all()


# GET ONE
def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id, Role.is_deleted == False).first()


# UPDATE
def update_role(db: Session, role_id: int, data, user_id: int):
    role = get_role(db, role_id)
    if not role:
        return None

    # ✅ OLD DATA
    old_data = {"name": role.name, "is_active": role.is_active}

    if data.name is not None:
        role.name = data.name.lower()

    if data.is_active is not None:
        role.is_active = data.is_active

    role.updated_by = user_id

    db.commit()
    db.refresh(role)

    # ✅ NEW DATA
    new_data = {"name": role.name, "is_active": role.is_active}

    # ✅ AUDIT LOG
    create_audit_log(
        db,
        user_id=user_id,
        action="update",
        module="role",
        record_id=role.id,
        old_data=old_data,
        new_data=new_data,
    )

    db.commit()

    return role


# DELETE (SOFT)
def delete_role(db: Session, role_id: int, user_id: int):
    role = get_role(db, role_id)
    if not role:
        return None

    # ✅ OLD DATA
    old_data = {"name": role.name}

    # 🔹 Soft delete: marks record as deleted and sets is_active=False (if present)
    role.soft_delete()
    role.updated_by = user_id

    db.commit()

    # ✅ AUDIT LOG
    create_audit_log(
        db,
        user_id=user_id,
        action="delete",
        module="role",
        record_id=role.id,
        old_data=old_data,
    )

    db.commit()

    return True
