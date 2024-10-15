from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import PaymentLink
from schemas import PaymentAnalyticsResponse
from config import SessionLocal
from models import *

router = APIRouter()

@router.get("/analytics", response_model=PaymentAnalyticsResponse)
async def get_payment_analytics(user: User = Depends(get_current_user)):
    db = SessionLocal()
    total_payments = db.query(PaymentLink).filter_by(user_id=user.id).count()
    total_success = db.query(PaymentLink).filter_by(user_id=user.id, status="complete").count()
    total_failure = db.query(PaymentLink).filter_by(user_id=user.id, status="failure").count()
    total_pending = db.query(PaymentLink).filter_by(user_id=user.id, status="pending").count()
    
    return PaymentAnalyticsResponse(
        total_payments=total_payments,
        total_success=total_success,
        total_failure=total_failure,
        total_pending=total_pending
    )
