from sqlalchemy.orm import declarative_base

Base = declarative_base()
ExchangeBase = declarative_base()

# 🔥 IMPORT ALL MODELS HERE (MANDATORY) .

# CRM Models
from app.models.user import User
from app.models.role import Role
from app.models.module_permission import ModulePermission
from app.models.role_permission import RolePermission
from app.models.user_permission import UserPermission

# Exchange Models
from app.models.companies import Company
from app.models.companies_location import CompanyLocation
from app.models.contacts import Contact
from app.models.topology_domain import TopologyDomain
from app.models.topology_master import TopologyMaster
from app.models.technology import Technology
from app.models.companies_technology import CompanyTechnology