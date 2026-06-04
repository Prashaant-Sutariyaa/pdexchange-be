from sqlalchemy.orm import Session
from app.models.user_permission import UserPermission


# 🔹 UPSERT (ONLY TRUE ALLOWED)
def upsert_user_permission(db: Session, data, updated_by: int):
    obj = db.query(UserPermission).filter(
        UserPermission.user_id == data.user_id,
        UserPermission.module_permission_id == data.module_permission_id
    ).first()

    if obj:
        # update existing
        obj.is_active = True   # always true
        obj.updated_by = updated_by
    else:
        # create new
        obj = UserPermission(
            user_id=data.user_id,
            module_permission_id=data.module_permission_id,
            is_active=True,
            created_by=updated_by,
            updated_by=updated_by
        )
        db.add(obj)

    db.commit()
    db.refresh(obj)

    return obj


# 🔹 GET (for UI)
def get_user_permissions(db: Session, user_id: int):
    return db.query(UserPermission).filter(
        UserPermission.user_id == user_id
    ).all()


# 🔹 DELETE (REMOVE OVERRIDE)
def delete_user_permission(db: Session, user_id: int, module_permission_id: int):
    obj = db.query(UserPermission).filter(
        UserPermission.user_id == user_id,
        UserPermission.module_permission_id == module_permission_id
    ).first()

    if not obj:
        return None

    db.delete(obj)
    db.commit()

    return True