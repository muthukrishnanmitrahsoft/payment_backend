import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///./test.db"
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
SUCCESS_URL = os.getenv("SUCCESS_URL")
CANCEL_URL = os.getenv("CANCEL_URL")
END_POINT = os.getenv("END_POINT")
CORE_URL = os.getenv("CORE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
