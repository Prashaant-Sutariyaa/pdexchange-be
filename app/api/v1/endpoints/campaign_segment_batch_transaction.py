from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.core.permissions import check_permission

from app.services.campaign_segment_batch_transaction_service import (
    get_transactions,
    get_transaction,
)

router = APIRouter(
    prefix="/campaign-segment-batch-transactions",
    tags=["Campaign Segment Batch Transactions"],
)


# ============================================================
# 🔹 GET ALL
# ============================================================
@router.get(
    "/",
    dependencies=[
        Depends(
            check_permission(
                "campaign",
                "view",
            )
        )
    ],
)
def read_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_transactions(db)


# ============================================================
# 🔹 GET ONE
# ============================================================
@router.get(
    "/{transaction_id}",
    dependencies=[
        Depends(
            check_permission(
                "campaign",
                "view",
            )
        )
    ],
)
def read_one(
    transaction_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    transaction = get_transaction(db, transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Campaign segment batch transaction not found",
        )

    return transaction
