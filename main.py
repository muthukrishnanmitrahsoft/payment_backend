from fastapi import FastAPI
from payment import router as payment_router
from analytics import router as analytics_router
from config import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:3000", 
    "http://localhost:3001",# React app (or whatever port it's running on)
    "https://payment-frontend-phi.vercel.app"
    # Add more origins if necessary
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Create the database
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(payment_router)
app.include_router(analytics_router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
