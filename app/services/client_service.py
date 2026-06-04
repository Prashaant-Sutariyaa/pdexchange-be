import base64
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.client import Client
from app.models.user import User


# 🔹 ISO FORMAT FUNCTION
def iso_now():
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


# 🔹 FORMAT RESPONSE
def format_client(c: Client):
    return {
        "id": c.id,
        "client_code": c.client_code,
        "name": c.name,
        "address": c.address,
        "country": c.country,
        "assigned_to": c.assigned_to,
        "contract_file_name": c.contract_file_name,
        # CONTACT
        "first_name": c.first_name,
        "last_name": c.last_name,
        "contact_designation": c.contact_designation,
        "contact_email": c.contact_email,
        "contact_office_number": c.contact_office_number,
        "contact_mobile_number": c.contact_mobile_number,
        # BILLING
        "billing_name": c.billing_name,
        "billing_address": c.billing_address,
        "billing_email": c.billing_email,
        "billing_terms": c.billing_terms,
        # FLAGS
        "is_active": c.is_active,
        "is_deleted": c.is_deleted,
        # METADATA (ISO FORMAT)
        "created_at": (
            c.created_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if c.created_at
            else None
        ),
        "created_by": c.created_by,
        "updated_at": (
            c.updated_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            if c.updated_at
            else None
        ),
        "updated_by": c.updated_by,
    }


# 🔹 CREATE
def create_client(db: Session, data, user_id: int):

    # ✅ 1. CHECK ASSIGNED USER
    user = db.query(User).filter(User.id == data.assigned_to).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assigned user does not exist",
        )

    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned user is deleted"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned user is inactive"
        )

    # ✅ 2. CHECK DUPLICATE NAME
    existing = db.query(Client).filter(Client.name.ilike(data.name)).first()

    if existing:
        if existing.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Client exists but is deleted. Restore instead of creating.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Client already exists"
            )

    # ✅ FILE
    file_data = None
    if data.contract_file:
        file_data = base64.b64decode(data.contract_file)

    now = datetime.now(timezone.utc)

    client = Client(
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
        # ✅ SAME VALUES
        created_at=now,
        updated_at=now,
        created_by=user_id,
        updated_by=user_id,
        is_active=True,
        is_deleted=False,
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    # 🔹 GENERATE CLIENT CODE (PV01, PV02...)
    client.client_code = f"PV{str(client.id).zfill(2)}"

    db.commit()
    db.refresh(client)

    return format_client(client)


def get_clients_list(db: Session, is_active: bool = None):
    query = db.query(Client).filter(Client.is_deleted == False)

    if is_active is not None:
        query = query.filter(Client.is_active == is_active)

    return query.order_by(Client.id.asc()).all()


# 🔹 GET ALL
def get_clients(db: Session, is_active: bool = None):
    query = db.query(Client).filter(Client.is_deleted == False)

    # 🔹 FILTER (ACTIVE / INACTIVE)
    if is_active is not None:
        query = query.filter(Client.is_active == is_active)

    clients = query.order_by(Client.created_at.desc()).all()

    return [format_client(c) for c in clients]


# 🔹 GET ONE
def get_client(db: Session, client_id: int):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.is_deleted == False)
        .first()
    )

    if not client:
        return None

    data = format_client(client)

    if client.contract_file:
        data["contract_file"] = base64.b64encode(client.contract_file).decode("utf-8")
    else:
        data["contract_file"] = None

    return data


# 🔹 DOWNLOAD FILE
def get_client_file(db: Session, client_id: int):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.is_deleted == False)
        .first()
    )

    if not client or not client.contract_file:
        return None

    return client


# 🔹 UPDATE
def update_client(db: Session, client_id: int, data, user_id: int):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.is_deleted == False)
        .first()
    )

    if not client:
        return None

    # ✅ DUPLICATE CHECK (if name updated)
    if data.name:
        existing = (
            db.query(Client)
            .filter(Client.name.ilike(data.name), Client.id != client_id)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Client name already exists",
            )

    # ✅ ASSIGNED USER CHECK
    if data.assigned_to:
        user = db.query(User).filter(User.id == data.assigned_to).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assigned user does not exist",
            )

    # 🔹 UPDATE FIELDS
    for field, value in data.dict(exclude_unset=True).items():
        if field == "contract_file" and value:
            setattr(client, field, base64.b64decode(value))
        else:
            setattr(client, field, value)

    # ✅ UPDATE METADATA
    client.updated_by = user_id
    client.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(client)

    return format_client(client)


# 🔹 DELETE
def delete_client(db: Session, client_id: int, user_id: int):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.is_deleted == False)
        .first()
    )

    if not client:
        return None

    # 🔹 Soft delete: marks record as deleted and sets is_active=False (if present)
    client.soft_delete()
    client.updated_by = user_id
    client.updated_at = datetime.now(timezone.utc)

    db.commit()

    return True
