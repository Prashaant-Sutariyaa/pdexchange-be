from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.services.user_access_service import get_user_permissions

router = APIRouter(prefix="/user-access", tags=["User Access"])


@router.get("/")
def get_access(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    permissions = get_user_permissions(db, user)

    return {
        "permissions": permissions
    }