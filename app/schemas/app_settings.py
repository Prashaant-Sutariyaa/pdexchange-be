from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AppSettingCreate(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class AppSettingUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class AppSettingResponse(BaseModel):
    id: int
    key: str
    value: str
    description: Optional[str]

    is_active: bool
    is_deleted: bool
    
    created_by: Optional[int]   # ✅ ADD THIS
    updated_by: Optional[int]   # ✅ ADD THIS

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True