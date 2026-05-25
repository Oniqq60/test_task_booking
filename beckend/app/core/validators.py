import re
from datetime import date

PHONE_PATTERNS = [
    r"^\+7\d{10}$",  # E.164: +79991234567
    r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$",  # +7 (999) 123-45-67
]

def validate_phone(phone: str) -> bool:
    return any(re.match(p, phone) for p in PHONE_PATTERNS)

def validate_dates(check_in: date, check_out: date) -> tuple[bool, str | None]:
    today = date.today()
    if check_in < today:
        return False, "check_in cannot be in the past"
    if check_out <= check_in:
        return False, "check_out must be after check_in"
    if check_out < today:
        return False, "Dates cannot be in the past"
    return True, None