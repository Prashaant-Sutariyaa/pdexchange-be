from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
import re

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.services.campaign_service import (
    create_campaign,
    get_campaigns,
    get_campaign,
    update_campaign,
    delete_campaign,
    get_campaign_file,
)

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post("/", dependencies=[Depends(check_permission("campaign", "create"))])
def create(
    data: CampaignCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return create_campaign(db, data, user.id)


@router.get("/", dependencies=[Depends(check_permission("campaign", "view"))])
def read_all(
    page: int = None,
    limit: int = None,
    status: str = None,
    search: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_campaigns(
        db=db,
        page=page,
        limit=limit,
        status=status,
        search=search,
        start_date=start_date, 
        end_date=end_date,
    )


@router.get(
    "/{campaign_id}", dependencies=[Depends(check_permission("campaign", "view"))]
)
def read_one(
    campaign_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    campaign = get_campaign(db, campaign_id)

    if not campaign:
        raise HTTPException(404, "Campaign not found")

    return campaign


# 🔥 DOWNLOAD
@router.get(
    "/download/{campaign_id}",
    dependencies=[Depends(check_permission("campaign", "download"))],
)
def download_file(
    campaign_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    campaign = get_campaign_file(db, campaign_id)

    if not campaign:
        raise HTTPException(404, "Campaign or file not found")

    filename = campaign.campaign_document_name or "download"
    filename = re.sub(r"[^\x00-\x7F]+", "", filename)

    if not filename.strip():
        filename = "download"

    return StreamingResponse(
        io.BytesIO(campaign.campaign_document),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.patch(
    "/{campaign_id}", dependencies=[Depends(check_permission("campaign", "edit"))]
)
def update(
    campaign_id: int,
    data: CampaignUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    campaign = update_campaign(db, campaign_id, data, user.id)

    if not campaign:
        raise HTTPException(404, "Campaign not found")

    return campaign


@router.delete(
    "/{campaign_id}", dependencies=[Depends(check_permission("campaign", "delete"))]
)
def delete(
    campaign_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    result = delete_campaign(db, campaign_id, user.id)

    if not result:
        raise HTTPException(404, "Campaign not found")

    return {"message": "Campaign deleted successfully"}
