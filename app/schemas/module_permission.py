from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ModulePermissionCreate(BaseModel):
    module_name: str
    menu_name: Optional[str] = None
    permission_name: str
    description: Optional[str] = None
    is_active: bool = True


class ModulePermissionUpdate(BaseModel):
    module_name: Optional[str] = None
    menu_name: Optional[str] = None
    permission_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ModulePermissionResponse(BaseModel):
    id: int
    module_name: str
    menu_name: Optional[str]
    permission_name: str
    description: Optional[str]
    is_active: bool
    created_by: Optional[int]
    updated_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True