from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db, create_tables
from app.routers import auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def on_startup():
    # Create tables if they don't exist
    create_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to Family Network API", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Family Network API"}

@app.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
    try:
        # Simple query to check database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
