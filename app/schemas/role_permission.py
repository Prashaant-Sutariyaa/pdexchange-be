from pydantic import BaseModel


class RolePermissionUpsert(BaseModel):
    role_id: int
    module_permission_id: int
    is_active: bool