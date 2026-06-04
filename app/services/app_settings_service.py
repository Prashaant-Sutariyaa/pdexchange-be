from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.app_settings import AppSetting


# CREATE
def create_setting(db: Session, data, user_id: int):
    key = data.key.lower()

    existing = db.query(AppSetting).filter(func.lower(AppSetting.key) == key).first()

    if existing:
        if existing.is_deleted:
            return "deleted"
        return "exists"

    obj = AppSetting(
        key=key,
        value=data.value,
        description=data.description,
        is_active=data.is_active,
        created_by=user_id,
        updated_by=user_id,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# GET ALL
def get_settings(db: Session):
    return (
        db.query(AppSetting)
        .filter(AppSetting.is_deleted == False)
        .order_by(AppSetting.created_at.desc())
        .all()
    )


# GET ONE
def get_setting(db: Session, key: str):
    return (
        db.query(AppSetting)
        .filter(AppSetting.key == key.lower(), AppSetting.is_deleted == False)
        .first()
    )


# UPDATE
def update_setting(db: Session, key: str, data, user_id: int):
    obj = get_setting(db, key)

    if not obj:
        return None

    if data.value is not None:
        obj.value = data.value

    if data.description is not None:
        obj.description = data.description

    if data.is_active is not None:
        obj.is_active = data.is_active

    obj.updated_by = user_id

    db.commit()
    db.refresh(obj)

    return obj


# DELETE (SOFT)
def delete_setting(db: Session, key: str, user_id: int):
    obj = get_setting(db, key)

    if not obj:
        return None

    # 🔹 Soft delete: marks record as deleted and sets is_active=False (if present)
    obj.soft_delete()
    obj.updated_by = user_id

    db.commit()

    return True
