from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.department import Department


# CREATE
def create_department(db: Session, data, user_id: int):
    name = data.name.lower()   # ✅ normalize

    existing = db.query(Department).filter(
        func.lower(Department.name) == name
    ).first()

    if existing:
        if hasattr(existing, "is_deleted") and existing.is_deleted:
            return "deleted"
        return "exists"

    dept = Department(
        name=name,
        is_active=data.is_active,
        created_by=user_id,
        updated_by=user_id
    )

    db.add(dept)
    db.commit()
    db.refresh(dept)

    return dept


def get_departments(db: Session, is_active: bool = None, is_deleted: bool = False):
    query = db.query(Department)

    # 🔹 filter deleted (default = not deleted)
    if is_deleted is not None:
        query = query.filter(Department.is_deleted == is_deleted)

    # 🔹 optional active filter
    if is_active is not None:
        query = query.filter(Department.is_active == is_active)

    return query.order_by(Department.created_at.desc()).all()


# GET ONE
def get_department(db: Session, dept_id: int):
    return db.query(Department).filter(
        Department.id == dept_id,
        Department.is_deleted == False   # ✅ ADD
    ).first()


# UPDATE
def update_department(db: Session, dept_id: int, data, user_id: int):
    dept = get_department(db, dept_id)

    if not dept:
        return None

    if data.name is not None:
        dept.name = data.name.lower()   # ✅ normalize

    if data.is_active is not None:
        dept.is_active = data.is_active

    dept.updated_by = user_id

    db.commit()
    db.refresh(dept)

    return dept


# DELETE (SOFT DELETE 🔥)
def delete_department(db: Session, dept_id: int, user_id: int):
    dept = get_department(db, dept_id)

    if not dept:
        return None

    # 🔹 Soft delete: marks record as deleted and sets is_active=False (if present)
    dept.soft_delete()
    dept.updated_by = user_id

    db.commit()

    return True