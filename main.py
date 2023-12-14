from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.routers import router
from app.database import Base, engine  # Import Base and engine

# Create FastAPI app
app = FastAPI()

# Allow all origins to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your router
app.include_router(router)

# Create the database tables
Base.metadata.create_all(bind=engine)  # Create tables before running the app
