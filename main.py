from fastapi import FastAPI
from payment import router as payment_router
from config import *
from analytics import router as analytics_router
from config import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
core_url = CORE_URL


origins = ["*"]

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
