"""
Input validation utilities.
"""
from datetime import datetime
from typing import Optional, Tuple


def validate_date_range(start_date: Optional[datetime], end_date: Optional[datetime]) -> Tuple[bool, str]:
    """Validate date range inputs."""
    if start_date and end_date:
        if start_date > end_date:
            return False, "Start date must be before end date."
    return True, ""


def validate_required_field(value: any, field_name: str) -> Tuple[bool, str]:
    """Validate that a required field is not empty."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} is required."
    return True, ""


def validate_severity(severity: str) -> Tuple[bool, str]:
    """Validate defect severity."""
    valid_severities = ["Critical", "High", "Medium", "Low"]
    if severity not in valid_severities:
        return False, f"Severity must be one of: {', '.join(valid_severities)}"
    return True, ""


def validate_status(status: str, valid_statuses: list) -> Tuple[bool, str]:
    """Validate status field."""
    if status not in valid_statuses:
        return False, f"Status must be one of: {', '.join(valid_statuses)}"
    return True, ""



