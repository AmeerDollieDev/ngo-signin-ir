import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?[0-9\s\-()]{7,20}$")


def validate_signin(name: str, email: str, phone: str) -> list[str]:
    """Return a list of validation error messages. Empty list means valid."""
    errors = []

    if not name or not name.strip():
        errors.append("Name is required.")
    elif len(name.strip()) > 120:
        errors.append("Name is too long.")

    if not email or not EMAIL_RE.match(email.strip()):
        errors.append("A valid email address is required.")

    if not phone or not PHONE_RE.match(phone.strip()):
        errors.append("A valid phone number is required.")

    return errors
