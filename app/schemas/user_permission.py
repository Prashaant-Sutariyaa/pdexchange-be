from pydantic import BaseModel


class UserPermissionUpsert(BaseModel):
    user_id: int
    module_permission_id: int
    is_active: bool = True