from app.services.sentinel.validators.validation_result import (
    ValidationResult,
)

EMAIL_VALIDATION_STATUS = {
    "valid",
    "invalid",
    "catch-all",
    "catch_all",
    "ok",
    "apollo verify",
}


EMAIL_STATUS = {
    "delivered",
    "opened",
    "clicked",
    "unsubscribed",
    "hard bounce",
    "soft bounce",
}


QUALITY_STATUS = {
    "qualified",
    "disqualified",
}


DBR_STATUS = {
    "yes",
    "no",
}


MIS_STATUS = {
    "RTD",
    "TBD",
    "delivered",
    "accepted",
    "internal rejected",
    "client rejected",
    "High CPC",
}


class DepartmentValidator:

    @staticmethod
    def validate(
        department: str,
        row: dict,
        cache: dict,
    ):

        department = (department or "").strip().lower()

        # ====================================================
        # DATAOPS
        # ====================================================

        if department == "dataops":

            status = (row.get("email_validation_status") or "").strip().lower()

            if status:

                if status not in EMAIL_VALIDATION_STATUS:

                    return ValidationResult.invalid(
                        ("Invalid Email " "Validation Status"),
                        row,
                    )

        # ====================================================
        # EMAIL
        # ====================================================

        elif department == "email":

            status = (row.get("email_status") or "").strip().lower()

            if status:

                if status not in {s.lower() for s in EMAIL_STATUS}:

                    return ValidationResult.invalid(
                        "Invalid Email Status",
                        row,
                    )

        # ====================================================
        # QUALITY
        # ====================================================

        elif department == "quality":

            status = (row.get("quality_status") or "").strip().lower()

            if status:

                if status not in {s.lower() for s in QUALITY_STATUS}:

                    return ValidationResult.invalid(
                        "Invalid Quality Status",
                        row,
                    )

        # ====================================================
        # DBR
        # ====================================================

        elif department == "dbr":

            status = (row.get("dbr_status") or "").strip().lower()

            if status:

                if status not in {s.lower() for s in DBR_STATUS}:

                    return ValidationResult.invalid(
                        "Invalid DBR Status",
                        row,
                    )

        # ====================================================
        # VOICE VERIFICATION
        # ====================================================

        elif department == "vv" or department == "voice verification":

            disposition = (row.get("vv_disposition") or "").strip()

            if disposition:

                disposition_status = cache["vv_dispositions"].get(disposition.lower())

                if not disposition_status:

                    return ValidationResult.invalid(
                        "Invalid VV Disposition",
                        row,
                    )

        # ====================================================
        # MIS
        # ====================================================

        elif department == "mis":

            status = (row.get("mis_status") or "").strip().lower()

            if status:

                if status not in {s.lower() for s in MIS_STATUS}:

                    return ValidationResult.invalid(
                        "Invalid MIS Status",
                        row,
                    )

        return ValidationResult.valid(row)
