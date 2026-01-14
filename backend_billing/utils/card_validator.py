import re
from datetime import datetime
from typing import Optional, Dict


CARD_PATTERNS = {
    "visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
    "mastercard": r"^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$",
    "amex": r"^3[47][0-9]{13}$",
    "discover": r"^6(?:011|5[0-9]{2})[0-9]{12}$",
    "diners": r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
    "jcb": r"^(?:2131|1800|35\d{3})\d{11}$",
}


def luhn_checksum(card_number: str) -> bool:
    if not card_number.isdigit():
        return False

    digits = [int(d) for d in card_number]
    checksum = 0

    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0


def detect_card_type(card_number: str) -> Optional[str]:
    card_number = card_number.replace(" ", "").replace("-", "")

    for card_type, pattern in CARD_PATTERNS.items():
        if re.match(pattern, card_number):
            return card_type

    return None


def validate_card_number(card_number: str) -> Dict[str, any]:
    errors = []
    clean_number = card_number.replace(" ", "").replace("-", "")

    if not clean_number:
        errors.append("Card number is required")
        return {"valid": False, "card_type": None, "errors": errors}

    if not clean_number.isdigit():
        errors.append("Card number must contain only digits")
        return {"valid": False, "card_type": None, "errors": errors}

    if len(clean_number) < 13 or len(clean_number) > 19:
        errors.append("Card number must be between 13 and 19 digits")

    card_type = detect_card_type(clean_number)
    if not card_type:
        errors.append("Unknown or unsupported card type")

    if not luhn_checksum(clean_number):
        errors.append("Invalid card number (failed Luhn check)")

    return {
        "valid": len(errors) == 0,
        "card_type": card_type,
        "errors": errors
    }


def validate_expiry(month: int, year: int) -> Dict[str, any]:
    errors = []

    if not isinstance(month, int) or month < 1 or month > 12:
        errors.append("Invalid month (must be 1-12)")
        return {"valid": False, "expired": False, "errors": errors}

    if year < 100:
        year += 2000

    current_year = datetime.now().year
    if year < current_year or year > current_year + 20:
        errors.append(f"Invalid year (must be between {current_year} and {current_year + 20})")

    current_date = datetime.now()
    expiry_date = datetime(year, month, 1)

    if expiry_date.year < current_date.year or \
       (expiry_date.year == current_date.year and expiry_date.month < current_date.month):
        errors.append("Card has expired")
        return {"valid": False, "expired": True, "errors": errors}

    return {
        "valid": len(errors) == 0,
        "expired": False,
        "errors": errors
    }


def validate_cvv(cvv: str, card_type: Optional[str] = None) -> Dict[str, any]:
    errors = []

    if not cvv:
        errors.append("CVV is required")
        return {"valid": False, "errors": errors}

    if not cvv.isdigit():
        errors.append("CVV must contain only digits")
        return {"valid": False, "errors": errors}

    expected_length = 4 if card_type == "amex" else 3

    if len(cvv) != expected_length:
        errors.append(f"CVV must be {expected_length} digits for {card_type or 'this card type'}")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_full_card(card_number: str, expiry_month: int, expiry_year: int,
                       cvv: str) -> Dict[str, any]:
    card_validation = validate_card_number(card_number)
    expiry_validation = validate_expiry(expiry_month, expiry_year)
    cvv_validation = validate_cvv(cvv, card_validation.get("card_type"))

    all_errors = []
    if card_validation["errors"]:
        all_errors.extend([f"Card: {err}" for err in card_validation["errors"]])
    if expiry_validation["errors"]:
        all_errors.extend([f"Expiry: {err}" for err in expiry_validation["errors"]])
    if cvv_validation["errors"]:
        all_errors.extend([f"CVV: {err}" for err in cvv_validation["errors"]])

    return {
        "valid": card_validation["valid"] and expiry_validation["valid"] and cvv_validation["valid"],
        "card_type": card_validation["card_type"],
        "expired": expiry_validation.get("expired", False),
        "errors": all_errors,
        "details": {
            "card_number": card_validation,
            "expiry": expiry_validation,
            "cvv": cvv_validation
        }
    }
