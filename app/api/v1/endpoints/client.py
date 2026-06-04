from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
from typing import Optional
import re

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission  # ✅ ADD THIS

from app.schemas.client import ClientCreate, ClientUpdate
from app.services.client_service import (
    create_client,
    get_clients,
    get_client,
    update_client,
    delete_client,
    get_client_file,
    get_clients_list,
)

router = APIRouter(prefix="/clients", tags=["Clients"])


# 🔹 CREATE
@router.post(
    "/", dependencies=[Depends(check_permission("client", "create"))]  # ✅ ADD
)
def create(
    data: ClientCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return create_client(db, data, user.id)


# 🚀 LIST API (LIGHTWEIGHT)
@router.get("/list", dependencies=[Depends(get_current_user)])
def client_list(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    clients = get_clients_list(db, is_active)

    return [{"id": c.id, "client_code": c.client_code, "name": c.name} for c in clients]


# 🔹 GET ALL
@router.get("/", dependencies=[Depends(check_permission("client", "view"))])  # ✅ ADD
def read_all(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_clients(db, is_active)


# 🔹 GET ONE
@router.get(
    "/{client_id}", dependencies=[Depends(check_permission("client", "view"))]  # ✅ ADD
)
def read_one(
    client_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    client = get_client(db, client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


# 🔹 DOWNLOAD FILE
@router.get(
    "/download/{client_id}",
    dependencies=[Depends(check_permission("client", "download"))],  # ✅ ADD
)
def download_file(
    client_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    client = get_client_file(db, client_id)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client or file not found"
        )

    if not client.contract_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No file available for this client",
        )

    filename = client.contract_file_name or "download"
    filename = re.sub(r"[^\x00-\x7F]+", "", filename)

    if not filename.strip():
        filename = "download"

    return StreamingResponse(
        io.BytesIO(client.contract_file),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# 🔹 UPDATE
@router.patch(
    "/{client_id}", dependencies=[Depends(check_permission("client", "edit"))]  # ✅ ADD
)
def update(
    client_id: int,
    data: ClientUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    client = update_client(db, client_id, data, user.id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


# 🔹 DELETE
@router.delete(
    "/{client_id}",
    dependencies=[Depends(check_permission("client", "delete"))],  # ✅ ADD
)
def delete(
    client_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    result = delete_client(db, client_id, user.id)

    if not result:
        raise HTTPException(status_code=404, detail="Client not found")

    return {"message": "Client deleted successfully"}
