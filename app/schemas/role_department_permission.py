from pydantic import BaseModel


class RDPUpset(BaseModel):
    role_id: int
    department_id: int
    module_permission_id: int
    is_active: bool