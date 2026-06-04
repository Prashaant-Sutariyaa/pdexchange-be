import re

from app.services.sentinel.validators.validation_result import (
    ValidationResult,
)


EMAIL_REGEX = re.compile(
    r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
)


class CommonValidator:

    @staticmethod
    def validate(
        department: str,
        row: dict,
    ):

        # ====================================================
        # NORMALIZATION
        # ====================================================

        normalized_row = {}

        for key, value in row.items():

            if isinstance(value, str):

                value = value.strip()
                value = value.strip("-")

                if key.lower() == "email":
                    value = value.lower()

                if value == "":
                    value = None

            normalized_row[key] = value

        # ====================================================
        # WORK EMAIL
        # ====================================================

        email = normalized_row.get("email")

        if not email:
            return ValidationResult.invalid(
                "Work Email missing",
                normalized_row,
            )

        if not EMAIL_REGEX.match(email):
            return ValidationResult.invalid(
                "Invalid email format",
                normalized_row,
            )

        # ====================================================
        # BATCH VALIDATION
        # ====================================================

        if department != "DataOps":

            batch_code = normalized_row.get("batch_code")

            if not batch_code:
                return ValidationResult.invalid(
                    "Batch Code required",
                    normalized_row,
                )

        return ValidationResult.valid(normalized_row)