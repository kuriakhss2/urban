from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict
from datetime import datetime
import uuid

# Payment Transaction Models
class PaymentTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    amount: float
    currency: str = "usd"
    customer_email: Optional[EmailStr] = None
    payment_status: str = "pending"  # pending, paid, failed, expired
    status: str = "initiated"  # initiated, completed, cancelled, expired
    metadata: Optional[Dict[str, str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Stripe Checkout Request Models
class CheckoutRequest(BaseModel):
    order_id: str
    customer_email: EmailStr
    origin_url: str

class CheckoutStatusRequest(BaseModel):
    session_id: str