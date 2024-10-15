from sqlalchemy import Column, Integer, String, Float, DateTime
from config import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

async def get_current_user():
    # Logic to get the current user, returning User model
    return User(id=1, username="testuser")  # Example user

class PaymentLink(Base):
    __tablename__ = "payment_links"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    currency = Column(String)
    description = Column(String)
    expiration = Column(DateTime)
    payment_url = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer)

