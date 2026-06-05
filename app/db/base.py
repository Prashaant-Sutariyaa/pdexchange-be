from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 🔥 IMPORT ALL MODELS HERE (MANDATORY)
from app.models.user import User
from app.models.role import Role
from app.models.module_permission import ModulePermission
from app.models.role_permission import RolePermission
from app.models.user_permission import UserPermission