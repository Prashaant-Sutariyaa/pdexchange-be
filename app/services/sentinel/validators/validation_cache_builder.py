from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.models.department import Department
from app.models.campaign_segment_batch import CampaignSegmentBatch
from app.models.campaign_segment_batch_transaction import (
    CampaignSegmentBatchTransaction,
)
from app.models.disposition import Disposition


class ValidationCacheBuilder:

    @staticmethod
    def build(
        db: Session,
        department: str,
        campaign_code: str | None = None,
    ):

        cache = {
            "agents": {},
            "email_seen": set(),
            "linkedin_seen": set(),
            "name_domain_seen": set(),
            "name_company_seen": set(),
            # VV DISPOSITION MAP
            "vv_dispositions": {},
        }

        # ====================================================
        # NORMALIZE DEPARTMENT
        # ====================================================

        department = (department or "").strip().lower()

        # ====================================================
        # AGENTS CACHE
        # ====================================================

        users = (
            db.query(
                User,
                Role.name.label("role_name"),
                Department.name.label("department_name"),
            )
            .join(Role, Role.id == User.role_id)
            .join(Department, Department.id == User.department_id)
            .filter(
                User.is_active == True,
                User.is_deleted == False,
                Role.is_active == True,
                Role.is_deleted == False,
                Department.is_active == True,
                Department.is_deleted == False,
            )
            .all()
        )

        for user, role_name, department_name in users:

            cache["agents"][user.email.strip().lower()] = {
                "id": user.id,
                "role": role_name,
                "department": department_name,
            }

        # ====================================================
        # DATAOPS DUPLICATE CACHE
        # ====================================================

        if department == "dataops" and campaign_code:

            # ================================================
            # FETCH ALL BATCHES OF CAMPAIGN
            # ================================================

            batch_rows = (
                db.query(CampaignSegmentBatch.batch_code)
                .filter(CampaignSegmentBatch.campaign_code == campaign_code)
                .all()
            )

            batch_codes = [row.batch_code for row in batch_rows if row.batch_code]

            # ================================================
            # NO BATCHES FOUND
            # ================================================

            if not batch_codes:
                return cache

            # ================================================
            # FETCH EXISTING TRANSACTIONS
            # ================================================

            rows = (
                db.query(
                    CampaignSegmentBatchTransaction.email,
                    CampaignSegmentBatchTransaction.contact_li_profile,
                    CampaignSegmentBatchTransaction.first_name,
                    CampaignSegmentBatchTransaction.last_name,
                    CampaignSegmentBatchTransaction.domain,
                    CampaignSegmentBatchTransaction.tal_company_name,
                )
                .filter(CampaignSegmentBatchTransaction.batch_code.in_(batch_codes))
                .all()
            )

            # ================================================
            # BUILD DUPLICATE SETS
            # ================================================

            for row in rows:

                # --------------------------------------------
                # EMAIL
                # --------------------------------------------

                if row.email:

                    cache["email_seen"].add(row.email.strip().lower())

                # --------------------------------------------
                # LINKEDIN
                # --------------------------------------------

                if row.contact_li_profile:

                    cache["linkedin_seen"].add(row.contact_li_profile.strip().lower())

                # --------------------------------------------
                # FIRST + LAST + DOMAIN
                # --------------------------------------------

                if row.first_name and row.last_name and row.domain:

                    key = (
                        f"{row.first_name.strip().lower()}|"
                        f"{row.last_name.strip().lower()}|"
                        f"{row.domain.strip().lower()}"
                    )

                    cache["name_domain_seen"].add(key)

                # --------------------------------------------
                # FIRST + LAST + COMPANY
                # --------------------------------------------

                if row.first_name and row.last_name and row.tal_company_name:

                    key = (
                        f"{row.first_name.strip().lower()}|"
                        f"{row.last_name.strip().lower()}|"
                        f"{row.tal_company_name.strip().lower()}"
                    )

                    cache["name_company_seen"].add(key)

        # ====================================================
        # VV DISPOSITIONS
        # ====================================================

        dispositions = (
            db.query(
                Disposition.call_disposition,
                Disposition.sentinel_status,
            )
            .filter(Disposition.is_deleted == False)
            .all()
        )

        for disposition in dispositions:

            if disposition.call_disposition:

                cache["vv_dispositions"][
                    disposition.call_disposition.strip().lower()
                ] = ((disposition.sentinel_status or "").strip().lower())

        return cache
