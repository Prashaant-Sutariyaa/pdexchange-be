from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.services.audit_log_service import create_audit_log


def authenticate_user(db: Session, email: str, password: str):
    user = (
        db.query(User)
        .filter(User.email == email.lower(), User.is_deleted == False)
        .first()
    )

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def create_user(db: Session, data, user_id: int | None):
    email = data.email.lower()

    existing = db.query(User).filter(User.email == email).first()

    if existing:
        if existing.is_deleted:
            return "deleted"
        return "exists"

    try:
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=email,
            password=hash_password(data.password),
            mobile_number=data.mobile_number,
            job_title=data.job_title,
            work_location=data.work_location,
            role_id=data.role_id,
            department_id=data.department_id,
            is_active=True,
            is_deleted=False,
            created_by=user_id,
            updated_by=user_id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        create_audit_log(
            db,
            user_id=user_id,
            action="create",
            module="user",
            record_id=user.id,
            new_data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
        )
        db.commit()
        return user

    except Exception:
        db.rollback()
        return "exists"


def get_users(
    db: Session,
    is_active: bool = None,
    is_deleted: bool = False,
    page: int | None = None,
    limit: int | None = None,
):

    query = db.query(User)

    # ========================================================
    # 🔹 FILTERS
    # ========================================================

    if is_deleted is not None:

        query = query.filter(User.is_deleted == is_deleted)

    if is_active is not None:

        query = query.filter(User.is_active == is_active)

    # ========================================================
    # 🔹 TOTAL
    # ========================================================

    total = query.count()

    # ========================================================
    # 🔹 PAGINATION
    # ========================================================

    if page and limit:

        offset = (page - 1) * limit

        users = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()

    else:

        users = query.order_by(User.created_at.desc()).all()

    # ========================================================
    # 🔹 RESPONSE
    # ========================================================

    return {
        "data": users,
        "page": page,
        "limit": limit,
        "total": total,
    }


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()


def update_user(db: Session, user_id: int, data, updated_by: int):
    user = get_user(db, user_id)
    if not user:
        return None

    # ✅ Capture OLD DATA
    old_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role_id": user.role_id,
        "department_id": user.department_id,
    }

    for key, value in data.dict(exclude_unset=True).items():

        if key == "email":
            continue

        if key == "password":
            value = hash_password(value)

        setattr(user, key, value)

    user.updated_by = updated_by

    db.commit()
    db.refresh(user)

    # ✅ Capture NEW DATA
    new_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role_id": user.role_id,
        "department_id": user.department_id,
    }

    # ✅ AUDIT LOG
    create_audit_log(
        db,
        user_id=updated_by,
        action="update",
        module="user",
        record_id=user.id,
        old_data=old_data,
        new_data=new_data,
    )

    db.commit()

    return user


def delete_user(db: Session, user_id: int, updated_by: int):
    user = get_user(db, user_id)
    if not user:
        return None

    # ✅ OLD DATA
    old_data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    # 🔹 Soft delete: marks record as deleted and sets is_active=False (if present)
    user.soft_delete()
    user.updated_by = updated_by

    db.commit()

    # ✅ AUDIT LOG
    create_audit_log(
        db,
        user_id=updated_by,
        action="delete",
        module="user",
        record_id=user.id,
        old_data=old_data,
    )

    db.commit()

    return True
