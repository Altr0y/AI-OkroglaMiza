# Testing the Billing Service

## Quick Start

1. Start the service:
```bash
docker-compose up backend_billing
```

2. Test the health endpoint:

**PowerShell (Windows):**
```powershell
Invoke-RestMethod http://localhost:5001/api/health
```

**Bash/curl (Linux/Mac):**
```bash
curl http://localhost:5001/api/health
```

## Testing with PowerShell (Windows) - One-Line Commands

### 1. Verify Full Card (Valid Visa)
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/verify" -Method POST -ContentType "application/json" -Body (@{card_number="4532015112830366";expiry_month=12;expiry_year=2027;cvv="123"} | ConvertTo-Json)
```

Expected response:
```json
{
  "valid": true,
  "card_type": "visa",
  "expired": false,
  "errors": []
}
```

### 2. Verify Full Card (Valid Mastercard)
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/verify" -Method POST -ContentType "application/json" -Body (@{card_number="5425233430109903";expiry_month=6;expiry_year=2028;cvv="789"} | ConvertTo-Json)
```

### 3. Verify Full Card (Valid Amex with 4-digit CVV)
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/verify" -Method POST -ContentType "application/json" -Body (@{card_number="374245455400126";expiry_month=3;expiry_year=2029;cvv="1234"} | ConvertTo-Json)
```

### 4. Detect Card Type
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/detect-type" -Method POST -ContentType "application/json" -Body (@{card_number="5425233430109903"} | ConvertTo-Json)
```

### 5. Verify Card Number Only
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/verify-number" -Method POST -ContentType "application/json" -Body (@{card_number="4532015112830366"} | ConvertTo-Json)
```

### 6. Test Invalid Card (Should Fail)
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/verify" -Method POST -ContentType "application/json" -Body (@{card_number="1234567890123456";expiry_month=12;expiry_year=2027;cvv="123"} | ConvertTo-Json)
```

### 7. Verify Expiry Date
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/verify-expiry" -Method POST -ContentType "application/json" -Body (@{expiry_month=12;expiry_year=2027} | ConvertTo-Json)
```

### 8. Verify CVV
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/verify-cvv" -Method POST -ContentType "application/json" -Body (@{cvv="123";card_type="visa"} | ConvertTo-Json)
```

## Testing with curl (Linux/Mac/Git Bash)

### 1. Verify Full Card (Valid Visa)
```bash
curl -X POST http://localhost:5001/api/card/verify \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366",
    "expiry_month": 12,
    "expiry_year": 2025,
    "cvv": "123"
  }'
```

Expected response:
```json
{
  "valid": true,
  "card_type": "visa",
  "expired": false,
  "errors": []
}
```

### 2. Verify Full Card (Valid Mastercard)
```bash
curl -X POST http://localhost:5001/api/card/verify \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "5425233430109903",
    "expiry_month": 6,
    "expiry_year": 2026,
    "cvv": "789"
  }'
```

### 3. Verify Full Card (Valid Amex with 4-digit CVV)
```bash
curl -X POST http://localhost:5001/api/card/verify \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "374245455400126",
    "expiry_month": 3,
    "expiry_year": 2027,
    "cvv": "1234"
  }'
```

### 4. Verify Invalid Card (Fails Luhn Check)
```bash
curl -X POST http://localhost:5001/api/card/verify \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "1234567890123456",
    "expiry_month": 12,
    "expiry_year": 2025,
    "cvv": "123"
  }'
```

Expected response:
```json
{
  "valid": false,
  "card_type": null,
  "expired": false,
  "errors": [
    "Card: Unknown or unsupported card type",
    "Card: Invalid card number (failed Luhn check)"
  ]
}
```

### 5. Verify Expired Card
```bash
curl -X POST http://localhost:5001/api/card/verify \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366",
    "expiry_month": 1,
    "expiry_year": 2024,
    "cvv": "123"
  }'
```

### 6. Verify Card Number Only
```bash
curl -X POST http://localhost:5001/api/card/verify-number \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366"
  }'
```

### 7. Detect Card Type
```bash
curl -X POST http://localhost:5001/api/card/detect-type \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "5425233430109903"
  }'
```

Expected response:
```json
{
  "card_type": "mastercard"
}
```

### 8. Verify Expiry Date
```bash
curl -X POST http://localhost:5001/api/card/verify-expiry \
  -H "Content-Type: application/json" \
  -d '{
    "expiry_month": 12,
    "expiry_year": 2025
  }'
```

### 9. Verify CVV
```bash
curl -X POST http://localhost:5001/api/card/verify-cvv \
  -H "Content-Type: application/json" \
  -d '{
    "cvv": "123",
    "card_type": "visa"
  }'
```

## Testing with Python Script

Run the included test script:
```bash
cd backend_billing
python test_validator.py
```

This will run comprehensive tests on all validation functions.

## Testing with Swagger UI

Visit `http://localhost:5001/apidocs/` in your browser for an interactive API documentation and testing interface.

## Test Card Numbers

| Card Type   | Number              | CVV  | Expiry      |
|-------------|---------------------|------|-------------|
| Visa        | 4532015112830366    | 123  | 12/2025     |
| Visa        | 4556737586899855    | 456  | 06/2026     |
| Mastercard  | 5425233430109903    | 789  | 09/2027     |
| Mastercard  | 2221000000000009    | 123  | 03/2025     |
| Amex        | 374245455400126     | 1234 | 12/2026     |
| Discover    | 6011000991001201    | 123  | 08/2025     |
| Diners      | 36227206271667      | 123  | 11/2026     |
| JCB         | 3528000700000000    | 123  | 05/2027     |

## PowerShell Commands (Windows)

For Windows users, use these PowerShell alternatives:

### Verify Full Card
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/verify" `
  -Method POST `
  -ContentType "application/json" `
  -Body (@{
    card_number = "4532015112830366"
    expiry_month = 12
    expiry_year = 2025
    cvv = "123"
  } | ConvertTo-Json)
```

### Detect Card Type
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/card/detect-type" `
  -Method POST `
  -ContentType "application/json" `
  -Body (@{
    card_number = "5425233430109903"
  } | ConvertTo-Json)
```

## Expected Error Scenarios

### 1. Missing Required Fields
```bash
curl -X POST http://localhost:5001/api/card/verify \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4532015112830366"
  }'
```

Response: `400 Bad Request` with error message

### 2. Invalid Month
```bash
curl -X POST http://localhost:5001/api/card/verify-expiry \
  -H "Content-Type: application/json" \
  -d '{
    "expiry_month": 13,
    "expiry_year": 2025
  }'
```

### 3. Non-numeric Card Number
```bash
curl -X POST http://localhost:5001/api/card/verify-number \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "abcd-efgh-ijkl-mnop"
  }'
```

## Integration Testing

To test the integration with your frontend or other services:

1. Ensure the service is running on port 5001
2. Update your frontend environment to include:
   ```
   NEXT_PUBLIC_BILLING_URL=http://localhost:5001
   ```
3. Make API calls from your application using the endpoints documented above