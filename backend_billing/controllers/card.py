from flask import Blueprint, request, jsonify

from utils.card_validator import (
    validate_card_number,
    validate_expiry,
    validate_cvv,
    validate_full_card,
    detect_card_type
)

card_bp = Blueprint("card", __name__)


@card_bp.post("/card/verify")
def verify_card():
    """Verify Credit Card
    Validates credit card information using Luhn algorithm and pattern matching.
    ---
    tags:
      - Card Verification
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - card_number
            - expiry_month
            - expiry_year
            - cvv
          properties:
            card_number:
              type: string
              example: "4532015112830366"
              description: Credit card number (can include spaces or hyphens)
            expiry_month:
              type: integer
              example: 12
              description: Expiration month (1-12)
            expiry_year:
              type: integer
              example: 2025
              description: Expiration year (2-digit or 4-digit)
            cvv:
              type: string
              example: "123"
              description: CVV/CVC code (3 digits for most cards, 4 for Amex)
            cardholder_name:
              type: string
              example: "John Doe"
              description: Name on the card (optional for verification)
    responses:
      200:
        description: Validation results
        schema:
          type: object
          properties:
            valid:
              type: boolean
              example: true
            card_type:
              type: string
              example: "visa"
            expired:
              type: boolean
              example: false
            errors:
              type: array
              items:
                type: string
              example: []
      400:
        description: Missing required fields
    """
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    card_number = data.get("card_number", "")
    expiry_month = data.get("expiry_month")
    expiry_year = data.get("expiry_year")
    cvv = data.get("cvv", "")

    if not card_number:
        return jsonify(error="card_number is required"), 400
    if expiry_month is None:
        return jsonify(error="expiry_month is required"), 400
    if expiry_year is None:
        return jsonify(error="expiry_year is required"), 400
    if not cvv:
        return jsonify(error="cvv is required"), 400

    result = validate_full_card(card_number, expiry_month, expiry_year, cvv)

    return jsonify(result), 200


@card_bp.post("/card/verify-number")
def verify_card_number():
    """Verify Card Number Only
    Validates only the card number using Luhn algorithm and detects card type.
    ---
    tags:
      - Card Verification
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - card_number
          properties:
            card_number:
              type: string
              example: "4532015112830366"
              description: Credit card number
    responses:
      200:
        description: Validation results
        schema:
          type: object
          properties:
            valid:
              type: boolean
              example: true
            card_type:
              type: string
              example: "visa"
            errors:
              type: array
              items:
                type: string
              example: []
      400:
        description: Missing card_number
    """
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    card_number = data.get("card_number", "")

    if not card_number:
        return jsonify(error="card_number is required"), 400

    result = validate_card_number(card_number)
    return jsonify(result), 200


@card_bp.post("/card/verify-expiry")
def verify_expiry():
    """Verify Expiration Date
    Validates the card expiration date.
    ---
    tags:
      - Card Verification
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - expiry_month
            - expiry_year
          properties:
            expiry_month:
              type: integer
              example: 12
              description: Expiration month (1-12)
            expiry_year:
              type: integer
              example: 2025
              description: Expiration year (2-digit or 4-digit)
    responses:
      200:
        description: Validation results
        schema:
          type: object
          properties:
            valid:
              type: boolean
              example: true
            expired:
              type: boolean
              example: false
            errors:
              type: array
              items:
                type: string
              example: []
      400:
        description: Missing required fields
    """
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    expiry_month = data.get("expiry_month")
    expiry_year = data.get("expiry_year")

    if expiry_month is None:
        return jsonify(error="expiry_month is required"), 400
    if expiry_year is None:
        return jsonify(error="expiry_year is required"), 400

    result = validate_expiry(expiry_month, expiry_year)
    return jsonify(result), 200


@card_bp.post("/card/verify-cvv")
def verify_cvv_endpoint():
    """Verify CVV Code
    Validates the CVV/CVC code.
    ---
    tags:
      - Card Verification
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - cvv
          properties:
            cvv:
              type: string
              example: "123"
              description: CVV/CVC code
            card_type:
              type: string
              example: "visa"
              description: Card type (optional, used to determine expected CVV length)
    responses:
      200:
        description: Validation results
        schema:
          type: object
          properties:
            valid:
              type: boolean
              example: true
            errors:
              type: array
              items:
                type: string
              example: []
      400:
        description: Missing cvv
    """
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    cvv = data.get("cvv", "")
    card_type = data.get("card_type")

    if not cvv:
        return jsonify(error="cvv is required"), 400

    result = validate_cvv(cvv, card_type)
    return jsonify(result), 200


@card_bp.post("/card/detect-type")
def detect_type():
    """Detect Card Type
    Detects the card type based on the card number pattern.
    ---
    tags:
      - Card Verification
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - card_number
          properties:
            card_number:
              type: string
              example: "4532015112830366"
              description: Credit card number
    responses:
      200:
        description: Card type detection result
        schema:
          type: object
          properties:
            card_type:
              type: string
              example: "visa"
              description: Detected card type or null if unknown
      400:
        description: Missing card_number
    """
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is required"), 400

    card_number = data.get("card_number", "")

    if not card_number:
        return jsonify(error="card_number is required"), 400

    card_type = detect_card_type(card_number)
    return jsonify(card_type=card_type), 200
