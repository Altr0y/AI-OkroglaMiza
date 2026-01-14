from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreditCard:
    """
    SECURITY NOTE: Never store full card numbers or CVV in production.
    Use PCI-DSS compliant payment processors (Stripe, PayPal).
    """
    id: Optional[int] = None
    user_id: str = ""
    last_four: str = ""
    card_type: str = ""
    expiry_month: int = 0
    expiry_year: int = 0
    cardholder_name: str = ""
    billing_address_line1: Optional[str] = None
    billing_address_line2: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_postal_code: Optional[str] = None
    billing_country: Optional[str] = None
    payment_token: Optional[str] = None
    is_default: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "last_four": self.last_four,
            "card_type": self.card_type,
            "expiry_month": self.expiry_month,
            "expiry_year": self.expiry_year,
            "cardholder_name": self.cardholder_name,
            "billing_address": {
                "line1": self.billing_address_line1,
                "line2": self.billing_address_line2,
                "city": self.billing_city,
                "state": self.billing_state,
                "postal_code": self.billing_postal_code,
                "country": self.billing_country,
            },
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class Transaction:
    id: Optional[int] = None
    user_id: str = ""
    card_id: Optional[int] = None
    amount: float = 0.0
    currency: str = "USD"
    status: str = "pending"
    processor: str = ""
    processor_transaction_id: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "card_id": self.card_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "processor": self.processor,
            "processor_transaction_id": self.processor_transaction_id,
            "description": self.description,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
