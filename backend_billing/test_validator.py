"""Simple test script for card validation utilities."""

from utils.card_validator import (
    validate_card_number,
    validate_expiry,
    validate_cvv,
    validate_full_card,
    detect_card_type
)


def test_card_validation():
    """Test various card validation scenarios."""
    print("Testing Credit Card Validation\n" + "="*50)

    # Test valid cards
    test_cards = [
        ("4532015112830366", "Visa"),
        ("5425233430109903", "Mastercard"),
        ("374245455400126", "Amex"),
        ("6011000991001201", "Discover"),
        ("36227206271667", "Diners"),
        ("3528000700000000", "JCB"),
    ]

    print("\n1. Testing Card Number Validation:")
    print("-" * 50)
    for card_number, expected_type in test_cards:
        result = validate_card_number(card_number)
        status = "✓" if result["valid"] else "✗"
        print(f"{status} {card_number}: {result['card_type']} (Expected: {expected_type})")
        if result["errors"]:
            print(f"  Errors: {result['errors']}")

    # Test invalid cards
    print("\n2. Testing Invalid Card Numbers:")
    print("-" * 50)
    invalid_cards = [
        "1234567890123456",  # Fails Luhn
        "4532015112830367",  # Fails Luhn (last digit wrong)
        "123",               # Too short
    ]

    for card_number in invalid_cards:
        result = validate_card_number(card_number)
        status = "✓" if not result["valid"] else "✗"
        print(f"{status} {card_number}: Valid={result['valid']}")
        if result["errors"]:
            print(f"  Errors: {result['errors']}")

    # Test expiry validation
    print("\n3. Testing Expiry Validation:")
    print("-" * 50)
    expiry_tests = [
        (12, 2025, "Future date"),
        (1, 2024, "Past date"),
        (13, 2025, "Invalid month"),
    ]

    for month, year, description in expiry_tests:
        result = validate_expiry(month, year)
        status = "✓" if result["valid"] else "✗"
        print(f"{status} {month}/{year} ({description}): Valid={result['valid']}")
        if result["errors"]:
            print(f"  Errors: {result['errors']}")

    # Test CVV validation
    print("\n4. Testing CVV Validation:")
    print("-" * 50)
    cvv_tests = [
        ("123", "visa", "Valid Visa CVV"),
        ("1234", "amex", "Valid Amex CVV"),
        ("12", "visa", "Too short"),
        ("abcd", "visa", "Non-numeric"),
    ]

    for cvv, card_type, description in cvv_tests:
        result = validate_cvv(cvv, card_type)
        status = "✓" if result["valid"] else "✗"
        print(f"{status} {cvv} for {card_type} ({description}): Valid={result['valid']}")
        if result["errors"]:
            print(f"  Errors: {result['errors']}")

    # Test full card validation
    print("\n5. Testing Full Card Validation:")
    print("-" * 50)
    full_test = validate_full_card("4532015112830366", 12, 2025, "123")
    print(f"Card Number: 4532015112830366")
    print(f"Expiry: 12/2025")
    print(f"CVV: 123")
    print(f"Valid: {full_test['valid']}")
    print(f"Card Type: {full_test['card_type']}")
    print(f"Expired: {full_test['expired']}")
    if full_test['errors']:
        print(f"Errors: {full_test['errors']}")

    print("\n" + "="*50)
    print("Testing Complete!")


if __name__ == "__main__":
    test_card_validation()
