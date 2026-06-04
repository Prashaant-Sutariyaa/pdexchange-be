from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DispositionResponse(BaseModel):
    id: int

    disposition_code: Optional[str]

    call_disposition: Optional[str]

    status: Optional[str]

    sentinel_status: Optional[str]

    churnable: Optional[bool]

    created_at: Optional[datetime]

    created_by: Optional[int]

    updated_at: Optional[datetime]

    updated_by: Optional[int]

    is_deleted: Optional[bool]

    class Config:
        from_attributes = True