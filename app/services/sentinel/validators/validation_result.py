from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    is_valid: bool
    reason: Optional[str] = None
    normalized_row: Optional[dict] = None


    @staticmethod
    def valid(row: dict):
        return ValidationResult(
            is_valid=True,
            reason=None,
            normalized_row=row,
        )


    @staticmethod
    def invalid(reason: str, row: dict):
        return ValidationResult(
            is_valid=False,
            reason=reason,
            normalized_row=row,
        )