from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.responses import StreamingResponse
import io
import re
from fastapi import status
from app.services.vendor_service import get_vendor_file
from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.schemas.vendor import VendorCreate, VendorUpdate
from app.services.vendor_service import (
    create_vendor,
    get_vendors,
    get_vendor,
    update_vendor,
    delete_vendor,
)

router = APIRouter(prefix="/vendors", tags=["Vendors"])


# Post Routes
@router.post("/", dependencies=[Depends(check_permission("vendor", "create"))])
def create(
    data: VendorCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return create_vendor(db, data, user.id)


# Get Routes
@router.get("/", dependencies=[Depends(check_permission("vendor", "view"))])
def read_all(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_vendors(db, is_active)


# Get One Route
@router.get("/{vendor_id}", dependencies=[Depends(check_permission("vendor", "view"))])
def read_one(
    vendor_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    vendor = get_vendor(db, vendor_id)

    if not vendor:
        raise HTTPException(404, "Vendor not found")

    return vendor


# Patch Route
@router.patch(
    "/{vendor_id}", dependencies=[Depends(check_permission("vendor", "edit"))]
)
def update(
    vendor_id: int,
    data: VendorUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    vendor = update_vendor(db, vendor_id, data, user.id)

    if not vendor:
        raise HTTPException(404, "Vendor not found")

    return vendor


# Delete Route
@router.delete(
    "/{vendor_id}", dependencies=[Depends(check_permission("vendor", "delete"))]
)
def delete(
    vendor_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    result = delete_vendor(db, vendor_id, user.id)

    if not result:
        raise HTTPException(404, "Vendor not found")

    return {"message": "Vendor deleted successfully"}


# Download File Route
@router.get(
    "/download/{vendor_id}",
    dependencies=[Depends(check_permission("vendor", "download"))],
)
def download_file(
    vendor_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    vendor = get_vendor_file(db, vendor_id)

    # ❌ NOT FOUND
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vendor or file not found"
        )

    # ❌ FILE NOT PRESENT
    if not vendor.contract_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No file available for this vendor",
        )

    # ✅ SAFE FILENAME
    filename = vendor.contract_file_name or "download"
    filename = re.sub(r"[^\x00-\x7F]+", "", filename)

    if not filename.strip():
        filename = "download"

    try:
        return StreamingResponse(
            io.BytesIO(vendor.contract_file),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while downloading file",
        )
