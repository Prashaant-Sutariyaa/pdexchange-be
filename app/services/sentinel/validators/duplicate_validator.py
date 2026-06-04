from app.services.sentinel.validators.validation_result import (
    ValidationResult,
)


class DuplicateValidator:

    @staticmethod
    def validate(
        row: dict,
        cache: dict,
    ):

        # ====================================================
        # EMAIL
        # ====================================================

        email = (
            row.get("email")
            or ""
        ).strip().lower()

        if email in cache["email_seen"]:

            return ValidationResult.invalid(
                "Duplicate Work Email",
                row,
            )

        cache["email_seen"].add(email)

        # ====================================================
        # LINKEDIN
        # ====================================================

        linkedin = (
            row.get("contact_li_profile")
            or ""
        ).strip().lower()

        if linkedin:

            if linkedin in cache["linkedin_seen"]:

                return ValidationResult.invalid(
                    "Duplicate LinkedIn Profile",
                    row,
                )

            cache["linkedin_seen"].add(linkedin)

        # ====================================================
        # NAME + DOMAIN
        # ====================================================

        first_name = (
            row.get("first_name")
            or ""
        ).strip().lower()

        last_name = (
            row.get("last_name")
            or ""
        ).strip().lower()

        domain = (
            row.get("domain")
            or ""
        ).strip().lower()

        if first_name and last_name and domain:

            key = (
                f"{first_name}|"
                f"{last_name}|"
                f"{domain}"
            )

            if key in cache["name_domain_seen"]:

                return ValidationResult.invalid(
                    "Duplicate First+Last+Domain",
                    row,
                )

            cache["name_domain_seen"].add(key)

        # ====================================================
        # NAME + COMPANY
        # ====================================================

        company = (
            row.get("tal_company_name")
            or ""
        ).strip().lower()

        if first_name and last_name and company:

            key = (
                f"{first_name}|"
                f"{last_name}|"
                f"{company}"
            )

            if key in cache["name_company_seen"]:

                return ValidationResult.invalid(
                    "Duplicate First+Last+Company",
                    row,
                )

            cache["name_company_seen"].add(key)

        return ValidationResult.valid(row)