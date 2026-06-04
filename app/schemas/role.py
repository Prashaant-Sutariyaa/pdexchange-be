from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RoleCreate(BaseModel):
    name: str
    is_active: bool = True


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class RoleResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    created_by: Optional[int]
    updated_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True