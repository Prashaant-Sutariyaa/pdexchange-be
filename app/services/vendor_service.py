import base64
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.vendor import Vendor
from app.models.user import User


# 🔹 FORMAT
def format_vendor(v: Vendor):
    return {
        "id": v.id,
        "vendor_code": v.vendor_code,

        "name": v.name,
        "address": v.address,
        "country": v.country,
        "assigned_to": v.assigned_to,

        "contract_file_name": v.contract_file_name,

        "first_name": v.first_name,
        "last_name": v.last_name,
        "contact_designation": v.contact_designation,
        "contact_email": v.contact_email,
        "contact_office_number": v.contact_office_number,
        "contact_mobile_number": v.contact_mobile_number,

        "billing_name": v.billing_name,
        "billing_address": v.billing_address,
        "billing_email": v.billing_email,
        "billing_terms": v.billing_terms,

        "is_active": v.is_active,
        "is_deleted": v.is_deleted,

        "created_at": v.created_at.isoformat(timespec="milliseconds").replace("+00:00", "Z") if v.created_at else None,
        "created_by": v.created_by,
        "updated_at": v.updated_at.isoformat(timespec="milliseconds").replace("+00:00", "Z") if v.updated_at else None,
        "updated_by": v.updated_by,
    }


# 🔹 CREATE
def create_vendor(db: Session, data, user_id: int):

    # USER CHECK
    user = db.query(User).filter(User.id == data.assigned_to).first()
    if not user:
        raise HTTPException(400, "Assigned user does not exist")
    if user.is_deleted:
        raise HTTPException(400, "Assigned user is deleted")
    if not user.is_active:
        raise HTTPException(400, "Assigned user is inactive")

    # DUPLICATE
    existing = db.query(Vendor).filter(
        Vendor.name.ilike(data.name),
        Vendor.is_deleted == False
    ).first()

    deleted_existing = db.query(Vendor).filter(
        Vendor.name.ilike(data.name),
        Vendor.is_deleted == True
    ).first()

    if existing:
        raise HTTPException(409, "Vendor already exists")

    if deleted_existing:
        raise HTTPException(409, "Vendor exists but is deleted")

    # FILE
    file_data = None
    if data.contract_file:
        file_data = base64.b64decode(data.contract_file)

    now = datetime.now(timezone.utc)

    vendor = Vendor(
        name=data.name,
        address=data.address,
        country=data.country,
        assigned_to=data.assigned_to,

        contract_file=file_data,
        contract_file_name=data.contract_file_name,

        first_name=data.first_name,
        last_name=data.last_name,
        contact_designation=data.contact_designation,
        contact_email=data.contact_email,
        contact_office_number=data.contact_office_number,
        contact_mobile_number=data.contact_mobile_number,

        billing_name=data.billing_name,
        billing_address=data.billing_address,
        billing_email=data.billing_email,
        billing_terms=data.billing_terms,

        created_at=now,
        updated_at=now,
        created_by=user_id,
        updated_by=user_id,

        is_active=True,
        is_deleted=False
    )

    db.add(vendor)
    db.commit()
    db.refresh(vendor)

    # CODE
    vendor.vendor_code = f"PVOP{str(vendor.id).zfill(2)}"

    db.commit()
    db.refresh(vendor)

    return format_vendor(vendor)


# 🔹 GET ALL
def get_vendors(db: Session, is_active: bool = None):
    query = db.query(Vendor).filter(Vendor.is_deleted == False)

    if is_active is not None:
        query = query.filter(Vendor.is_active == is_active)

    vendors = query.order_by(Vendor.created_at.desc()).all()

    return [format_vendor(v) for v in vendors]


# 🔹 GET ONE
def get_vendor(db: Session, vendor_id: int):
    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_deleted == False
    ).first()

    if not vendor:
        return None

    data = format_vendor(vendor)

    if vendor.contract_file:
        data["contract_file"] = base64.b64encode(vendor.contract_file).decode("utf-8")
    else:
        data["contract_file"] = None

    return data


# 🔹 UPDATE
def update_vendor(db: Session, vendor_id: int, data, user_id: int):
    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_deleted == False
    ).first()

    if not vendor:
        return None

    if data.name:
        existing = db.query(Vendor).filter(
            Vendor.name.ilike(data.name),
            Vendor.id != vendor_id
        ).first()

        if existing:
            raise HTTPException(409, "Vendor name already exists")

    if data.assigned_to:
        user = db.query(User).filter(User.id == data.assigned_to).first()
        if not user:
            raise HTTPException(400, "Assigned user does not exist")

    for field, value in data.dict(exclude_unset=True).items():
        if field == "contract_file" and value:
            setattr(vendor, field, base64.b64decode(value))
        elif field != "is_deleted":
            setattr(vendor, field, value)

    vendor.updated_by = user_id
    vendor.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(vendor)

    return format_vendor(vendor)


# 🔹 DELETE
def delete_vendor(db: Session, vendor_id: int, user_id: int):
    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_deleted == False
    ).first()

    if not vendor:
        return None

    # 🔹 Soft delete: marks record as deleted and sets is_active=False (if present)
    vendor.soft_delete()
    vendor.updated_by = user_id
    vendor.updated_at = datetime.now(timezone.utc)

    db.commit()

    return True

def get_vendor_file(db: Session, vendor_id: int):
    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id,
        Vendor.is_deleted == False
    ).first()

    if not vendor or not vendor.contract_file:
        return None

    return vendor