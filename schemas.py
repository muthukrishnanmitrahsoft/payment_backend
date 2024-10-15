from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class PaymentLinkCreate(BaseModel):
    amount: float
    currency: str
    description: str
    expiration: datetime

class PaymentLinkResponse(BaseModel):
    id: int
    payment_url: str
    status: str
    created_at: datetime

class PaymentAnalyticsResponse(BaseModel):
    total_payments: int
    total_success: int
    total_failure: int
    total_pending: int
