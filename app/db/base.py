from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 🔥 IMPORT ALL MODELS HERE (MANDATORY)
from app.models.user import User
from app.models.role import Role
from app.models.department import Department
from app.models.module_permission import ModulePermission
from app.models.role_department_permission import RoleDepartmentPermission
from app.models.user_permission import UserPermission
from app.models.campaign_segment_batch import CampaignSegmentBatch
from app.models.campaign_segment_batch_transaction import CampaignSegmentBatchTransaction
from app.models.sentinel_job import SentinelJob
from app.models.sentinel_activity_log import SentinelActivityLog
from app.models.sentinel_agent_productivity import SentinelAgentProductivity
from app.models.disposition import Disposition