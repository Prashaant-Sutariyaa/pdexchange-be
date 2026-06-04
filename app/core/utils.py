from sqlalchemy.orm import Session
from app.models.department import Department


def get_department_id_by_name(db: Session, name: str):
    dept = db.query(Department).filter(Department.name == name).first()
    if not dept:
        return None
    return dept.id