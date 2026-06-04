from app.models.campaign_segment_batch_transaction import (
    CampaignSegmentBatchTransaction,
)
from app.services.sentinel.validators.validation_result import ValidationResult


class EligibilityValidator:

    @staticmethod
    def validate(
        db,
        department: str,
        row: dict,
        cache,
    ):

        # ====================================================
        # NORMALIZE DEPARTMENT
        # ====================================================

        department = (department or "").strip().lower()

        # ====================================================
        # DATAOPS
        # ====================================================

        if department == "dataops":

            return ValidationResult.valid(row)

        batch_code = row.get("batch_code")
        email = row.get("email")

        transaction = (
            db.query(CampaignSegmentBatchTransaction)
            .filter(
                CampaignSegmentBatchTransaction.batch_code == batch_code,
                CampaignSegmentBatchTransaction.email == email,
            )
            .first()
        )

        if not transaction:

            return ValidationResult.invalid(
                "No previous transaction found",
                row,
            )

        # ====================================================
        # EMAIL
        # ====================================================

        if department == "email":

            status = (transaction.email_validation_status or "").strip().lower()

            if status not in [
                "valid",
                "catch-all",
            ]:

                return ValidationResult.invalid(
                    "Logical stop at DataOps",
                    row,
                )

        # ====================================================
        # QUALITY
        # ====================================================

        elif department == "quality":

            status = (transaction.email_status or "").strip().lower()

            if status not in [
                "delivered",
                "opened",
                "clicked",
            ]:

                return ValidationResult.invalid(
                    "Logical stop at Email",
                    row,
                )

        # ====================================================
        # DBR
        # ====================================================

        elif department == "dbr":

            status = (transaction.quality_status or "").strip().lower()

            if status != "qualified":

                return ValidationResult.invalid(
                    "Logical stop at Quality",
                    row,
                )

        # ====================================================
        # VOICE VERIFICATION
        # ====================================================

        elif department == "vv" or department == "voice verification":

            status = (transaction.dbr_status or "").strip().lower()

            if status != "yes":

                return ValidationResult.invalid(
                    "Logical stop at DB Refresh",
                    row,
                )

        # ====================================================
        # MIS
        # ====================================================

        elif department == "mis":

            disposition = (transaction.vv_disposition or "").strip().lower()

            if not disposition:

                return ValidationResult.invalid(
                    "Logical stop at Voice Verification",
                    row,
                )

            disposition_status = cache["vv_dispositions"].get(disposition)

            if disposition_status != "valid":

                return ValidationResult.invalid(
                    "Logical stop at Voice Verification",
                    row,
                )

        return ValidationResult.valid(row)
