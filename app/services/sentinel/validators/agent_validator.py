from app.services.sentinel.validators.validation_result import (
    ValidationResult,
)

DEPARTMENT_AGENT_FIELDS = {
    "dataops": "dataops_agent",
    "email": "email_agent",
    "quality": "quality_agent",
    "dbr": "dbr_agent",
    "voice verification": "vv_agent",
    "vv": "vv_agent",
    "mis": "mis_agent",
}


# ============================================================
# ALLOWED AGENT DEPARTMENTS
# ============================================================

EXPECTED_DEPARTMENTS = {
    "dataops": {"DataOps"},
    "email": {"Email"},
    "quality": {"Quality"},
    "dbr": {"DBR", "DataOps"},
    "voice verification": {"Voice Verification"},
    "vv": {"Voice Verification"},
    "mis": {"MIS"},
}


class AgentValidator:

    @staticmethod
    def validate(
        department: str,
        row: dict,
        cache: dict,
    ):

        # ====================================================
        # AGENT FIELD
        # ====================================================

        agent_field = DEPARTMENT_AGENT_FIELDS.get(department)

        if not agent_field:

            return ValidationResult.valid(row)

        # ====================================================
        # AGENT EMAIL
        # ====================================================

        agent_email = (row.get(agent_field) or "").strip().lower()

        if not agent_email:

            return ValidationResult.invalid(
                f"{agent_field} missing",
                row,
            )

        # ====================================================
        # AGENT LOOKUP
        # ====================================================

        agent = cache["agents"].get(agent_email)

        if not agent:

            return ValidationResult.invalid(
                f"{agent_field} not found or inactive",
                row,
            )

        # ====================================================
        # ROLE
        # ====================================================

        role_name = (agent["role"] or "").strip().lower()

        # ====================================================
        # ALLOWED DEPARTMENTS
        # ====================================================

        allowed_departments = EXPECTED_DEPARTMENTS.get(
            department,
            set(),
        )

        # ====================================================
        # EXECUTIVE VALIDATION
        # ====================================================

        agent_department = (agent["department"] or "").strip()
        print(
            "AGENT:",
            agent_email,
            "ROLE:",
            role_name,
            "AGENT DEPARTMENT:",
            agent_department,
            "UPLOAD DEPARTMENT:",
            department,
            "ALLOWED:",
            allowed_departments,
        )

        if agent_department not in allowed_departments:

            allowed_text = ", ".join(sorted(allowed_departments))

            return ValidationResult.invalid(
                (f"{agent_field} must belong to " f"{allowed_text}"),
                row,
            )

        return ValidationResult.valid(row)
