from app.services.sentinel.validators.common_validator import CommonValidator
from app.services.sentinel.validators.agent_validator import AgentValidator
from app.services.sentinel.validators.eligibility_validator import EligibilityValidator
from app.services.sentinel.validators.duplicate_validator import DuplicateValidator
from app.services.sentinel.validators.validation_result import ValidationResult
from app.services.sentinel.validators.department_validator import DepartmentValidator


class ValidationService:

    @staticmethod
    def validate_row(
        db,
        department: str,
        row: dict,
        cache: dict,
    ):

        # ====================================================
        # NORMALIZE DEPARTMENT
        # ====================================================

        department = (department or "").strip().lower()

        # ====================================================
        # COMMON VALIDATION
        # ====================================================

        result = CommonValidator.validate(
            department,
            row,
        )

        if not result.is_valid:
            return result

        row = result.normalized_row

        # ====================================================
        # AGENT VALIDATION
        # ====================================================

        result = AgentValidator.validate(
            department,
            row,
            cache,
        )

        if not result.is_valid:
            return result

        # ====================================================
        # ELIGIBILITY VALIDATION
        # ====================================================

        result = EligibilityValidator.validate(
            db,
            department,
            row,
            cache,
        )

        if not result.is_valid:
            return result

        # ====================================================
        # DEPARTMENT VALIDATION
        # ====================================================

        result = DepartmentValidator.validate(
            department,
            row,
            cache,
        )

        if not result.is_valid:
            return result

        # ====================================================
        # DATAOPS DUPLICATES
        # ====================================================

        if department == "dataops":

            result = DuplicateValidator.validate(
                row,
                cache,
            )

            if not result.is_valid:
                return result

        return ValidationResult.valid(row)
