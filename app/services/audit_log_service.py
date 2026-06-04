from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    module: str,
    record_id: int,
    old_data: dict = None,
    new_data: dict = None
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        module=module,
        record_id=record_id,
        old_data=old_data,
        new_data=new_data
    )

    db.add(log)